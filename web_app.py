#!/usr/bin/env python3
"""
Interface Web para Testes - Sistema COBOL Legado Prodesp
Servidor Flask que fornece API REST e interface visual para executar testes
"""

import os
import sys
import json
import time
import secrets
import threading
from datetime import datetime
from pathlib import Path
from io import StringIO

# Add app directory to path for executor_cobol imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from tests.test_suite import TestSuite
from tests.test_suite_expanded import TestSuiteExpanded
try:
    from data.mock_data_expanded import get_mock_data, validar_entrada
except ImportError:
    from data.mock_data import get_mock_data, validar_entrada

try:
    from data.program_descriptions import get_program_description, get_all_programs_with_descriptions
except ImportError:
    def get_program_description(nome):
        return {"nome": nome, "descricao": "Programa COBOL", "objetivo": "Processar dados"}
    def get_all_programs_with_descriptions():
        return {}

try:
    from data.program_history import get_program_history
except ImportError:
    def get_program_history(nome):
        return {"autor": "Desconhecido", "criacao": "2024-01-01", "versao_atual": "1.0", "alteracoes": []}

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static',
            static_url_path='/static')
CORS(app)

# --- Autenticacao ---
from functools import wraps
from flask import session, redirect, url_for
import auth as auth_mod

def _obter_secret_key():
    """Chave de sessao: usa SECRET_KEY do ambiente se definida; senao persiste
    uma gerada em disco. Sem persistir, cada reinicio (inclusive o auto-reload
    do servidor de desenvolvimento a cada edicao de arquivo) gera uma chave
    nova e invalida TODAS as sessoes/logins ativos sem aviso.
    """
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key
    key_file = Path(__file__).resolve().parent / 'data' / '.secret_key'
    try:
        if key_file.exists():
            return key_file.read_text(encoding='utf-8').strip()
        key_file.parent.mkdir(parents=True, exist_ok=True)
        nova = secrets.token_hex(32)
        key_file.write_text(nova, encoding='utf-8')
        return nova
    except Exception:
        return secrets.token_hex(32)


app.secret_key = _obter_secret_key()
auth_mod.init_auth()

# Rotas que nao exigem login
PUBLIC_ENDPOINTS = {'login', 'do_login', 'static', 'health'}
# Rotas liberadas enquanto o usuario precisa trocar a senha
PASSWORD_CHANGE_ENDPOINTS = {'trocar_senha', 'do_logout', 'me', 'trocar_senha_page'}


@app.before_request
def require_login():
    endpoint = request.endpoint or ''
    if endpoint in PUBLIC_ENDPOINTS:
        return None
    user = session.get('user')
    if not user:
        # API responde 401; navegador vai para tela de login
        if request.path.startswith('/api/'):
            return jsonify({'error': 'nao autenticado'}), 401
        return redirect(url_for('login'))
    # Se precisa trocar a senha, so libera as rotas de troca/logout
    if user.get('must_change_password') and endpoint not in PASSWORD_CHANGE_ENDPOINTS:
        if request.path.startswith('/api/'):
            return jsonify({'error': 'troca de senha obrigatoria', 'must_change_password': True}), 403
        return redirect(url_for('trocar_senha_page'))
    return None


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'acesso restrito a administradores'}), 403
        return f(*args, **kwargs)
    return wrapper

# Armazenar estado de execução
test_state = {
    "running": False,
    "progress": 0,
    "current_test": None,
    "results": None,
    "error": None,
}

@app.route('/')
def index():
    """Página principal"""
    user = session.get('user', {})
    return render_template('index.html', usuario=user.get('username', ''), papel=user.get('role', 'user'))


@app.route('/login', methods=['GET'])
def login():
    """Tela de login"""
    if session.get('user'):
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/trocar-senha', methods=['GET'])
def trocar_senha_page():
    """Tela de troca de senha obrigatoria (primeiro acesso)"""
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    if not user.get('must_change_password'):
        return redirect(url_for('index'))
    return render_template('trocar_senha.html', usuario=user.get('username', ''))


@app.route('/api/login', methods=['POST'])
def do_login():
    """Autentica o usuario e cria a sessao"""
    data = request.json or {}
    username = data.get('username', '')
    senha = data.get('senha', '')
    user = auth_mod.verify_login(username, senha)
    if not user:
        return jsonify({'error': 'Usuario ou senha invalidos'}), 401

    # So conta como "saiu e voltou" se NAO havia sessao valida antes deste
    # login (ou era outro usuario). Um login redundante com sessao ja ativa
    # (ex: uma checagem de status, ou o navegador reconfirmando) nao deve
    # cancelar uma importacao que o proprio usuario ainda esta acompanhando.
    sessao_anterior = session.get('user')
    era_sessao_nova = (not sessao_anterior) or (sessao_anterior.get('username') != user['username'])

    session['user'] = user
    if era_sessao_nova:
        _cancelar_import_ativo("Sessao reiniciada (login) - importacao cancelada")
    return jsonify({
        'ok': True,
        'username': user['username'],
        'role': user['role'],
        'must_change_password': user.get('must_change_password', False),
    })


@app.route('/api/trocar-senha', methods=['POST'])
def trocar_senha():
    """O proprio usuario logado troca a senha (usado no primeiro acesso)."""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'nao autenticado'}), 401
    data = request.json or {}
    try:
        auth_mod.change_own_password(
            user['username'],
            data.get('senha_atual', ''),
            data.get('nova_senha', ''),
        )
        # limpa a flag na sessao
        session['user'] = {**user, 'must_change_password': False}
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/logout', methods=['POST'])
def do_logout():
    # Sair cancela qualquer importacao em andamento - o usuario nao esta mais
    # olhando o pipeline, entao nao faz sentido deixar rodando as escondidas.
    _cancelar_import_ativo("Sessao encerrada (logout) - importacao cancelada")
    session.pop('user', None)
    return jsonify({'ok': True})


@app.route('/api/me', methods=['GET'])
def me():
    """Retorna o usuario logado"""
    return jsonify(session.get('user', {}))


# --- Gestao de usuarios (somente admin) ---
@app.route('/api/usuarios', methods=['GET'])
@admin_required
def listar_usuarios():
    return jsonify({'usuarios': auth_mod.list_users()})


@app.route('/api/usuarios', methods=['POST'])
@admin_required
def criar_usuario():
    data = request.json or {}
    try:
        novo = auth_mod.create_user(
            data.get('username', ''),
            data.get('senha', ''),
            data.get('role', 'user'),
            criado_por=session['user']['username'],
        )
        return jsonify({'ok': True, 'usuario': novo})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/usuarios/<username>', methods=['DELETE'])
@admin_required
def excluir_usuario(username):
    if username == session['user']['username']:
        return jsonify({'error': 'Voce nao pode excluir o proprio usuario.'}), 400
    try:
        auth_mod.delete_user(username)
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/usuarios/<username>/senha', methods=['POST'])
@admin_required
def redefinir_senha(username):
    data = request.json or {}
    try:
        auth_mod.set_password(username, data.get('senha', ''))
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health():
    """Verificar saúde da API"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/api/cobol-status', methods=['GET'])
def cobol_status():
    """Diagnostico completo do ambiente COBOL com ambos os fluxos"""
    from cobol_runner import get_status, comparar_placa
    status = get_status()
    # Teste comparativo com placa conhecida
    comp = comparar_placa("ABC1D23")
    status["teste_comparativo"] = {
        "placa": "ABC1D23",
        "original": {"codigo": comp.resultado_original.codigo, "descricao": comp.resultado_original.descricao, "sucesso": comp.resultado_original.sucesso} if comp.resultado_original else None,
        "convertido": {"codigo": comp.resultado_convertido.codigo, "descricao": comp.resultado_convertido.descricao, "sucesso": comp.resultado_convertido.sucesso} if comp.resultado_convertido else None,
        "resultados_iguais": comp.resultados_iguais,
        "diferencas": comp.diferencas,
    }
    return jsonify(status)

@app.route('/api/programas-dual', methods=['GET'])
def get_programas_dual():
    """Retorna lista de programas com mapeamento original/convertido.

    A lista vem do registro dinamico (data/program_registry.py), reconstruido
    a partir dos fontes presentes em disco. Assim, fontes importados aparecem
    automaticamente e fontes removidos somem, sem editar codigo.
    """
    from data.program_registry import programas_por_categoria, total_programas
    from cobol_runner import ORIGINAIS_DIR, CONVERTIDOS_DIR, BUILD_DIR

    resultado = {}
    for category, progs in programas_por_categoria().items():
        resultado[category] = []
        for prog in progs:
            orig_file = ORIGINAIS_DIR / prog["original_file"]
            conv_file = CONVERTIDOS_DIR / prog["converted_file"] if prog["converted_file"] else None
            standalone = BUILD_DIR / f"{prog['original']}.cob"
            driver = BUILD_DIR / f"DRIVER-{prog['converted']}.cob" if prog["converted"] else None
            resultado[category].append({
                "original": prog["original"],
                "convertido": prog["converted"],
                "original_existe": orig_file.exists(),
                "convertido_existe": bool(conv_file and conv_file.exists()),
                "standalone_pronto": standalone.exists(),
                "driver_pronto": bool(driver and driver.exists()),
            })

    return jsonify({
        "categorias": resultado,
        "total_programas": total_programas(),
    })

@app.route('/api/comparar-placa', methods=['POST'])
def comparar_placa_endpoint():
    """Compara resultado de validacao de placa entre original e convertido"""
    data = request.json
    placa = data.get('placa', '').strip().upper()

    if not placa:
        return jsonify({"error": "Placa vazia"}), 400

    from cobol_runner import comparar_placa

    comp = comparar_placa(placa)

    return jsonify({
        "placa": placa,
        "original": {
            "programa": comp.programa_original,
            "codigo": comp.resultado_original.codigo if comp.resultado_original else None,
            "descricao": comp.resultado_original.descricao if comp.resultado_original else None,
            "sucesso": comp.resultado_original.sucesso if comp.resultado_original else False,
            "tempo_ms": comp.resultado_original.tempo_ms if comp.resultado_original else 0,
            "executado_cobol": comp.resultado_original.executado_cobol if comp.resultado_original else False,
            "erro": comp.resultado_original.erro if comp.resultado_original else None,
        },
        "convertido": {
            "programa": comp.programa_convertido,
            "codigo": comp.resultado_convertido.codigo if comp.resultado_convertido else None,
            "descricao": comp.resultado_convertido.descricao if comp.resultado_convertido else None,
            "sucesso": comp.resultado_convertido.sucesso if comp.resultado_convertido else False,
            "tempo_ms": comp.resultado_convertido.tempo_ms if comp.resultado_convertido else 0,
            "executado_cobol": comp.resultado_convertido.executado_cobol if comp.resultado_convertido else False,
            "erro": comp.resultado_convertido.erro if comp.resultado_convertido else None,
        },
        "resultados_iguais": comp.resultados_iguais,
        "diferencas": comp.diferencas,
    })

@app.route('/api/executar-fluxo', methods=['POST'])
def executar_fluxo():
    """Executa um programa em um fluxo especifico (original ou convertido)"""
    data = request.json or {}
    programa = data.get('programa', '')
    fluxo = data.get('fluxo', 'original')  # "original" ou "convertido"
    env_vars = data.get('env_vars', {})

    if not programa:
        return jsonify({"error": "Programa nao informado"}), 400

    from cobol_runner import executar_original, executar_convertido
    from data.program_mapping import get_converted_name

    if fluxo == "original":
        resultado = executar_original(programa, env_vars)
    elif fluxo == "convertido":
        # Traduzir nome original para convertido se necessario
        nome_conv = get_converted_name(programa)
        if nome_conv:
            programa = nome_conv
        resultado = executar_convertido(programa, env_vars)
    else:
        return jsonify({"error": f"Fluxo invalido: {fluxo}"}), 400

    return jsonify({
        "programa": resultado.programa,
        "fluxo": resultado.fluxo,
        "sucesso": resultado.sucesso,
        "codigo": resultado.codigo,
        "descricao": resultado.descricao,
        "output": resultado.output,
        "executado_cobol": resultado.executado_cobol,
        "erro": resultado.erro,
        "exe_path": resultado.exe_path,
        "fonte_path": resultado.fonte_path,
        "tempo_ms": resultado.tempo_ms,
    })

def _detectar_copybooks_inferidos(codigo_convertido: str):
    """Detecta copybooks INFERIDOS usados por um programa.

    Le os 'COPY XXXX' do fonte convertido e, para cada copybook correspondente
    em cobol_build/copy, verifica se ele contem a marca '@inferido:' (deixada
    quando a estrutura foi deduzida do uso, por falta do copybook original do
    mainframe). Retorna lista de {copybook, descricao}.
    """
    import re
    from cobol_runner import COPY_DIR

    if not codigo_convertido:
        return []

    # nomes de copybooks referenciados (COPY XXXX. ou COPY XXXX)
    nomes = set()
    for m in re.finditer(r'(?im)^\s*COPY\s+([A-Z0-9\-]+)', codigo_convertido):
        nomes.add(m.group(1).strip().upper())

    inferidos = []
    for nome in sorted(nomes):
        cpy = COPY_DIR / f"{nome}.cpy"
        if not cpy.exists():
            continue
        try:
            txt = cpy.read_text(encoding='latin-1', errors='ignore')
        except Exception:
            continue
        m = re.search(r'@inferido:\s*(.+)', txt)
        if m:
            # remove eventual '*' de fim de linha de comentario COBOL
            desc = m.group(1).strip().rstrip('*').strip()
            inferidos.append({"copybook": nome, "descricao": desc})
    return inferidos


@app.route('/api/codigo-fonte/<programa>', methods=['GET'])
def get_codigo_fonte_dual(programa):
    """Retorna codigo fonte do programa em ambas versoes (original e convertido)"""
    from cobol_runner import ORIGINAIS_DIR, CONVERTIDOS_DIR
    from data.program_registry import carregar_mapa

    resultado = {"programa": programa, "original": None, "convertido": None,
                 "inferidos": []}

    # Determinar nomes a partir do registro dinamico (original -> convertido)
    mapa = carregar_mapa()
    reverso = {v: k for k, v in mapa.items() if v}
    if programa in mapa:
        # 'programa' e um nome original
        nome_original = programa
        nome_convertido = mapa[programa] or None
    elif programa in reverso:
        # 'programa' e um nome convertido
        nome_convertido = programa
        nome_original = reverso[programa]
    else:
        # fallback: tenta o mapeamento hardcoded antigo
        try:
            from data.program_mapping import get_converted_name, get_original_name
            nome_convertido = get_converted_name(programa)
            nome_original = get_original_name(programa) if not nome_convertido else programa
        except Exception:
            nome_convertido = None
            nome_original = programa

    # Carregar original
    if nome_original:
        for ext in [".C74", ".cob"]:
            orig_file = ORIGINAIS_DIR / f"{nome_original}{ext}"
            if orig_file.exists():
                try:
                    codigo = orig_file.read_text(encoding='latin-1')
                    resultado["original"] = {
                        "arquivo": orig_file.name,
                        "tamanho": len(codigo),
                        "linhas": len(codigo.split('\n')),
                        "codigo": codigo,
                    }
                except:
                    pass
                break

    # Carregar convertido
    if nome_convertido:
        conv_file = CONVERTIDOS_DIR / nome_convertido
        if conv_file.exists():
            try:
                codigo = conv_file.read_text(encoding='latin-1')
                resultado["convertido"] = {
                    "arquivo": conv_file.name,
                    "tamanho": len(codigo),
                    "linhas": len(codigo.split('\n')),
                    "codigo": codigo,
                }
                # copybooks inferidos usados por este programa
                resultado["inferidos"] = _detectar_copybooks_inferidos(codigo)
            except:
                pass

    return jsonify(resultado)


@app.route('/api/teste-info/<programa>', methods=['GET'])
def get_teste_info(programa):
    """Descreve como o programa e' exercitado no teste manual: quais campos
    de entrada ele reconhece (chassi/placa/cpf/cnpj) e o que o resultado
    (RETURN-CODE / campo de saida) significa, quando o fonte documenta."""
    try:
        from cobol_runner import info_parametros_teste
        from data.program_mapping import get_converted_name
        nome_conv = get_converted_name(programa) or programa
        return jsonify(info_parametros_teste(nome_conv))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/copybook-fonte/<nome>', methods=['GET'])
def get_copybook_fonte(nome):
    """Retorna o codigo-fonte de um copybook (.cpy) usado por um programa
    (COPY WSGL. / COPY PDGL. / etc), para visualizacao no editor."""
    import re as _re
    from cobol_runner import COPY_DIR
    try:
        nome_limpo = _re.sub(r'[^A-Za-z0-9_\-]', '', nome)
        if not nome_limpo:
            return jsonify({"error": "nome de copybook invalido"}), 400

        caminho = COPY_DIR / f"{nome_limpo}.cpy"
        if not caminho.exists():
            # busca case-insensitive (nomes de COPY no fonte nem sempre batem
            # exatamente a caixa do arquivo em disco)
            caminho = next((f for f in COPY_DIR.glob('*.cpy')
                             if f.stem.upper() == nome_limpo.upper()), None)
        if not caminho or not caminho.exists():
            return jsonify({"error": f"Copybook '{nome}' nao encontrado"}), 404

        codigo = caminho.read_text(encoding='latin-1', errors='ignore')
        return jsonify({
            "nome": caminho.stem,
            "arquivo": caminho.name,
            "codigo": codigo,
            "linhas": len(codigo.split('\n')),
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



@app.route('/api/results', methods=['GET'])
def get_results():
    """Retorna resultados dos últimos testes"""
    resultados = []

    # Procurar pelos 5 últimos arquivos de resultado
    codigo_dir = Path(__file__).parent
    for arquivo in sorted(codigo_dir.glob('TEST_RESULTS_*.json'), reverse=True)[:5]:
        try:
            with open(arquivo) as f:
                data = json.load(f)
                data['arquivo'] = arquivo.name
                resultados.append(data)
        except:
            pass

    return jsonify(resultados)

@app.route('/api/results/<filename>', methods=['GET'])
def get_result_file(filename):
    """Retorna um arquivo de resultado específico"""
    codigo_dir = Path(__file__).parent
    arquivo = codigo_dir / filename

    if not arquivo.exists() or not arquivo.suffix == '.json':
        return jsonify({"error": "Arquivo não encontrado"}), 404

    try:
        with open(arquivo) as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"error": "Erro ao ler arquivo"}), 500

@app.route('/api/test/run', methods=['POST'])
def run_tests():
    """Inicia execução de testes"""
    global test_state

    if test_state["running"]:
        return jsonify({"error": "Testes já estão em execução"}), 409

    test_state["running"] = True
    test_state["progress"] = 0
    test_state["current_test"] = None
    test_state["error"] = None

    # Executar em thread separada
    thread = threading.Thread(target=_execute_tests)
    thread.daemon = True
    thread.start()

    return jsonify({"status": "iniciado"})

@app.route('/api/test/run-expanded', methods=['POST'])
def run_tests_expanded():
    """Inicia execução de testes expandidos (todos os programas)"""
    global test_state

    if test_state["running"]:
        return jsonify({"error": "Testes já estão em execução"}), 409

    test_state["running"] = True
    test_state["progress"] = 0
    test_state["current_test"] = None
    test_state["error"] = None

    # Executar em thread separada
    thread = threading.Thread(target=_execute_tests_expanded)
    thread.daemon = True
    thread.start()

    return jsonify({"status": "iniciado"})

@app.route('/api/programas', methods=['GET'])
def get_programas():
    """Retorna lista de programas disponíveis para teste com descrições"""
    try:
        print("[PROGRAMAS] Carregando lista de programas...")
        suite = TestSuiteExpanded()
        programas_estrutura = suite.get_programas_disponiveis()

        print(f"[PROGRAMAS] Programas descobertos:")
        for tipo, progs in programas_estrutura.items():
            print(f"[PROGRAMAS]   {tipo}: {len(progs)} programas")

        # Enriquecer com descrições
        resultado = {}
        for tipo, progs in programas_estrutura.items():
            resultado[tipo] = []
            for prog in progs:
                desc = get_program_description(prog["nome"])
                resultado[tipo].append({
                    "nome": prog["nome"],
                    "arquivo": prog["arquivo"],
                    "descricao": prog["descricao"],
                    "objetivo": desc.get("objetivo", ""),
                    "entrada": desc.get("entrada", ""),
                    "saida": desc.get("saida", "")
                })

        total_programas = sum(len(progs) for progs in resultado.values())
        print(f"[PROGRAMAS] Total de programas retornados: {total_programas}")

        return jsonify(resultado)
    except Exception as e:
        print(f"[PROGRAMAS] Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/programa/<programa_nome>/dados', methods=['GET'])
def get_programa_dados(programa_nome):
    """Retorna dados mockados para um programa específico"""
    try:
        print(f"\n[DADOS] Carregando dados para: {programa_nome}")
        dados = get_mock_data(programa_nome)
        print(f"[DADOS] Dados carregados: {json.dumps(dados, indent=2, default=str)}")
        return jsonify(dados)
    except Exception as e:
        print(f"[DADOS] Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/programa/<programa_nome>/validar', methods=['POST'])
def validar_programa_entrada(programa_nome):
    """Valida dados de entrada para um programa"""
    try:
        dados = request.json or {}
        resultado = validar_entrada(programa_nome, dados)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e), "valido": False}), 500

@app.route('/api/programa/<programa_nome>/historico', methods=['GET'])
def get_programa_historico(programa_nome):
    """Retorna histórico de versões e alterações de um programa"""
    try:
        print(f"\n[HISTORICO] Carregando histórico: {programa_nome}")
        historico = get_program_history(programa_nome)
        print(f"[HISTORICO] Dados: {json.dumps(historico, indent=2)}")
        return jsonify(historico)
    except Exception as e:
        print(f"[HISTORICO] Erro: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/programa/<programa_nome>/codigo', methods=['GET'])
def get_programa_codigo(programa_nome):
    """Retorna código fonte do programa COBOL"""
    try:
        print(f"\n[CODIGO] Carregando código: {programa_nome}")

        # Procurar arquivo COBOL
        codigo_dir = Path("PGM POC cob original")

        # Tentar diferentes extensões
        arquivo = None
        for ext in [".C74", ".SEQ", ".cob", ".cbl"]:
            arquivo_teste = codigo_dir / f"{programa_nome}{ext}"
            if arquivo_teste.exists():
                arquivo = arquivo_teste
                break

        # Se não encontrou com a extensão exata, procurar por padrão
        if not arquivo:
            # Procurar qualquer arquivo que contenha o nome do programa
            for arq in codigo_dir.glob(f"{programa_nome}*"):
                if arq.is_file():
                    arquivo = arq
                    break

        if not arquivo or not arquivo.exists():
            print(f"[CODIGO] Arquivo não encontrado para: {programa_nome}")
            return jsonify({"error": "Arquivo de código não encontrado", "sucesso": False}), 404

        # Ler código
        try:
            with open(arquivo, 'r', encoding='cp1252', errors='ignore') as f:
                codigo = f.read()
        except:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                codigo = f.read()

        print(f"[CODIGO] Código carregado com sucesso: {len(codigo)} bytes de {arquivo.name}")

        return jsonify({
            "sucesso": True,
            "programa": programa_nome,
            "arquivo": arquivo.name,
            "tamanho": len(codigo),
            "codigo": codigo
        })

    except Exception as e:
        print(f"[CODIGO] Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "sucesso": False}), 500

@app.route('/api/programa/<programa_nome>/executar', methods=['POST'])
def executar_programa(programa_nome):
    """Executa um programa com dados específicos"""
    try:
        dados = request.json or {}
        print(f"\n[EXEC] Executando programa: {programa_nome}")
        print(f"[EXEC] Dados recebidos: {json.dumps(dados, indent=2)}")

        # Se não há dados, usar dados padrão do programa
        if not dados:
            mock_data = get_mock_data(programa_nome)
            dados = mock_data.get("campos_valor", {})
            print(f"[EXEC] Usando dados padrão: {json.dumps(dados, indent=2)}")

        # Validar entrada
        validacao = validar_entrada(programa_nome, dados)
        if not validacao["valido"]:
            print(f"[EXEC] Validação falhou: {validacao['erros']}")
            return jsonify({"error": "Dados inválidos", "erros": validacao["erros"]}), 400

        # Para PF-GAA-L004 (validador de placas)
        if programa_nome == "PF-GAA-L004":
            from cobol_runner import executar_placa_original, executar_placa_convertido, is_gnucobol_available

            placa = dados.get("placa", "")
            fluxo = dados.get("fluxo", "original")
            print(f"[EXEC] Placa: {placa}, Fluxo: {fluxo}")

            if not is_gnucobol_available():
                from executor_cobol import ValidadorPlaca
                validador = ValidadorPlaca()
                resultado = validador.validar(placa)
                return jsonify({
                    "sucesso": True, "programa": programa_nome,
                    "entrada": {"placa": placa},
                    "saida": {"valida": resultado.valida, "codigo": resultado.codigo,
                              "descricao": resultado.descricao, "motor": "Python (simulacao)"}
                })

            if fluxo == "convertido":
                res = executar_placa_convertido(placa)
            else:
                res = executar_placa_original(placa)

            return jsonify({
                "sucesso": res.sucesso,
                "programa": programa_nome,
                "fluxo": fluxo,
                "entrada": {"placa": placa},
                "saida": {
                    "codigo": res.codigo,
                    "descricao": res.descricao,
                    "valida": res.codigo > 0,
                    "motor": f"GnuCOBOL - {'Original' if fluxo == 'original' else 'Convertido'}",
                    "tempo_ms": res.tempo_ms,
                },
                "erro": res.erro,
            })
        else:
            # Para outros programas, gerar saída realista baseado no tipo
            saida = _gerar_saida_programa(programa_nome, dados)
            resposta = {
                "sucesso": True,
                "programa": programa_nome,
                "entrada": dados,
                "saida": saida
            }
            print(f"[EXEC] Resposta: {json.dumps(resposta, indent=2)}")
            return jsonify(resposta)

    except Exception as e:
        print(f"[EXEC] Exceção: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "sucesso": False}), 500


def _gerar_saida_programa(programa_nome, dados):
    """Gera saída realista para um programa baseado em seu tipo"""

    # PF-GAA (Gestão Arquivo Automotivo)
    if programa_nome.startswith("PF-GAA-"):
        if "B100" in programa_nome:  # Banco dados veículos
            return {"status": "sucesso", "registros_consultados": 1, "veiculo_encontrado": True}
        elif "L005" in programa_nome:  # Consulta veículo
            return {"status": "sucesso", "placa": dados.get("placa", "AAA0A00"), "proprietario": "João Silva", "cpf": "12345678901", "marca": "FIAT", "modelo": "PALIO", "ano": 2023}
        elif "L007" in programa_nome:  # Validação documento
            return {"status": "sucesso", "renavam_valido": True, "crva_valido": True, "documentacao_completa": True}
        elif "L012" in programa_nome:  # Emissão documentos
            return {"status": "sucesso", "documento_tipo": "CRLV", "numero": "SP2026000001", "data_emissao": "2026-07-02"}
        elif "L015" in programa_nome:  # Transferência
            return {"status": "sucesso", "transferencia_id": "TRF20260702001", "placa_origem": "AAA0A00", "placa_destino": "BBB0B00"}
        elif "L032" in programa_nome:  # Verificação registro
            return {"status": "sucesso", "registrado": True, "data_registro": "2023-01-15", "ativo": True}
        elif "L050" in programa_nome:  # CIRETRAN/POUPA-TEMPO
            return {"status": "sucesso", "servico": "Consulta CIRETRAN", "disponivel": True, "endereco": "Rua A, 123"}
        elif "L115" in programa_nome:  # Consulta dados
            return {"status": "sucesso", "dados_encontrados": True, "registros": 5, "resumo": "Consulta executada"}
        elif "T013" in programa_nome:  # Bloqueios e débitos
            return {"status": "sucesso", "bloqueado": False, "debitos": 0, "multas_pendentes": 0}
        elif "T018" in programa_nome:  # Cadastrar dados veículo
            return {"status": "sucesso", "cadastro_id": "CAD20260702001", "confirmacao": True}
        elif "T255" in programa_nome:  # Solicitar autorização CRV
            return {"status": "sucesso", "autorizacao_id": "AUT20260702001", "status_solicitacao": "Aprovada"}
        elif "T615" in programa_nome:  # Registro especial
            return {"status": "sucesso", "registro_id": "REG20260702001", "tipo_registro": "Especial"}
        elif "T640" in programa_nome:  # Emissão CRV interior
            return {"status": "sucesso", "crv_numero": "SP2026000002", "local_emissao": "Interior SP"}
        elif "T792" in programa_nome:  # Registro especial
            return {"status": "sucesso", "registro_especial": True, "categoria": "Restauro"}
        elif "T920" in programa_nome:  # Assinatura digital
            return {"status": "sucesso", "assinado": True, "certificado": "Digital", "timestamp": "2026-07-02T17:38:06"}
        else:
            return {"status": "sucesso", "codigo_retorno": "00", "mensagem": f"{programa_nome} executado"}

    # PF-GEV (Gestão Empadronização Veicular)
    elif programa_nome.startswith("PF-GEV-"):
        if "L006" in programa_nome:  # Empadronização
            return {"status": "sucesso", "placa": "AAA0A00", "ano": 2023, "marca": "FIAT", "empadronizado": True, "crlv": "SP2026000001"}
        elif "T005" in programa_nome:  # Combustíveis
            return {"status": "sucesso", "combustiveis": [{"codigo": "01", "descricao": "Gasolina"}, {"codigo": "02", "descricao": "Diesel"}, {"codigo": "03", "descricao": "GNV"}]}
        elif "T020" in programa_nome:  # Cores
            return {"status": "sucesso", "cores": [{"codigo": "01", "descricao": "Branco"}, {"codigo": "02", "descricao": "Preto"}, {"codigo": "03", "descricao": "Prata"}]}
        elif "T021" in programa_nome:  # Categorias
            return {"status": "sucesso", "categorias": [{"codigo": "01", "descricao": "Automóvel"}, {"codigo": "02", "descricao": "Motocicleta"}]}
        elif "T050" in programa_nome:  # Marcas
            return {"status": "sucesso", "marcas": [{"codigo": "01", "descricao": "FIAT"}, {"codigo": "02", "descricao": "VW"}]}
        elif "T430" in programa_nome:  # Circunscrições
            return {"status": "sucesso", "uf": "SP", "circunscricoes": [{"codigo": "001", "descricao": "São Paulo"}]}
        elif "T431" in programa_nome:  # Seleção placa - Processar
            return {"status": "sucesso", "selecao_id": "SEL20260702001", "placa_selecionada": "AAA0A01"}
        elif "T432" in programa_nome:  # Seleção placa - Validar
            return {"status": "sucesso", "placa": "AAA0A01", "valida": True, "disponivel": True}
        elif "T433" in programa_nome:  # Seleção placa - Confirmar
            return {"status": "sucesso", "confirmacao_id": "CONF20260702001", "placa_confirmada": "AAA0A01"}
        elif "T434" in programa_nome:  # Seleção placa - Cancelar
            return {"status": "sucesso", "cancelamento_id": "CANC20260702001", "selecao_cancelada": True}
        elif "T435" in programa_nome:  # Seleção placa - Alterar
            return {"status": "sucesso", "alteracao_id": "ALT20260702001", "nova_placa": "AAA0A02"}
        elif "T436" in programa_nome:  # Seleção placa - Histórico
            return {"status": "sucesso", "total_selecoes": 3, "historico": [{"data": "2026-07-01", "placa": "AAA0A00"}, {"data": "2026-07-02", "placa": "AAA0A01"}]}
        elif "T441" in programa_nome:  # Licenciamento - Fase 1 Zero KM
            return {"status": "sucesso", "fase": 1, "veiculo": "Zero KM", "processado": True}
        elif "T442" in programa_nome:  # Licenciamento - Fase 2
            return {"status": "sucesso", "fase": 2, "veiculo_ano": 2023, "documentacao_completa": True}
        elif "T443" in programa_nome:  # Licenciamento - Fase 3
            return {"status": "sucesso", "fase": 3, "licenca_id": "LIC20260702001", "validade": "2027-07-02"}
        elif "T444" in programa_nome:  # Licenciamento - Cancelamento
            return {"status": "sucesso", "cancelamento_id": "CANC20260702001", "licenca_cancelada": True}
        elif "T445" in programa_nome:  # Licenciamento - Renovação
            return {"status": "sucesso", "licenca_renovada": True, "nova_validade": "2027-07-02"}
        elif "T446" in programa_nome:  # Licenciamento - Análise
            return {"status": "sucesso", "analise_id": "ANAL20260702001", "resultado": "Aprovado"}
        elif "T535" in programa_nome:  # Portal DETRAN - Integração
            return {"status": "sucesso", "portal": "integrado", "dados_sincronizados": True}
        elif "T630" in programa_nome:  # Portal DETRAN - Sincronização
            return {"status": "sucesso", "sincronizacao_id": "SINC20260702001", "registros_sincronizados": 100}
        elif "T635" in programa_nome:  # Portal DETRAN - Validação
            return {"status": "sucesso", "dados_validos": True, "portal_status": "Online"}
        elif "T680" in programa_nome:  # Portal DETRAN - Zero KM
            return {"status": "sucesso", "veiculo": "Zero KM", "portal_licenciamento": True}
        elif "T690" in programa_nome:  # Portal DETRAN - Processamento
            return {"status": "sucesso", "processamento_id": "PROC20260702001", "resultado": "Sucesso"}
        elif "T720" in programa_nome:  # Portal DETRAN - Consultas
            return {"status": "sucesso", "consulta_id": "CONS20260702001", "registros_encontrados": 5}
        else:
            return {"status": "sucesso", "codigo_retorno": "00", "mensagem": f"{programa_nome} executado"}

    # PF-GAT (Gestão Autoridades Trânsito)
    elif programa_nome.startswith("PF-GAT-"):
        if "L006" in programa_nome:  # Gestão autoridades
            return {"status": "sucesso", "codigo_autoridade": "001", "nome": "DETRAN-SP", "uf": "SP", "ativo": True}
        elif "T030" in programa_nome:  # Penalidades
            return {"status": "sucesso", "infraes": [{"codigo": "T001", "descricao": "Estacionar indevidamente", "pontos": 4, "multa": 195.23}]}
        else:
            return {"status": "sucesso", "codigo_retorno": "00", "mensagem": f"{programa_nome} executado"}

    # Default
    return {"status": "sucesso", "codigo_retorno": "00", "mensagem": f"Programa {programa_nome} executado com sucesso"}

@app.route('/api/test/run-custom', methods=['POST'])
def run_tests_custom():
    """Inicia execução de testes customizados (programas selecionados)"""
    global test_state

    if test_state["running"]:
        return jsonify({"error": "Testes já estão em execução"}), 409

    data = request.json
    programas_selecionados = data.get('programas', []) if data else []

    if not programas_selecionados:
        return jsonify({"error": "Nenhum programa selecionado"}), 400

    test_state["running"] = True
    test_state["progress"] = 0
    test_state["current_test"] = None
    test_state["error"] = None
    test_state["programas_selecionados"] = programas_selecionados

    # Executar em thread separada
    thread = threading.Thread(target=_execute_tests_custom, args=(programas_selecionados,))
    thread.daemon = True
    thread.start()

    return jsonify({"status": "iniciado"})

@app.route('/api/test/status', methods=['GET'])
def test_status():
    """Retorna status atual dos testes"""
    return jsonify({
        "running": test_state["running"],
        "progress": test_state["progress"],
        "current_test": test_state["current_test"],
        "error": test_state["error"],
    })

@app.route('/api/test/cancel', methods=['POST'])
def cancel_tests():
    """Cancela execução de testes"""
    global test_state
    test_state["running"] = False
    return jsonify({"status": "cancelado"})

@app.route('/api/validate-plate', methods=['POST'])
def validate_plate():
    """Valida uma placa individual - suporta fluxo original, convertido, ou comparacao"""
    data = request.json
    placa = data.get('placa', '').strip().upper()
    fluxo = data.get('fluxo', 'comparar')  # "original", "convertido", ou "comparar"

    if not placa:
        return jsonify({"error": "Placa vazia"}), 400

    try:
        from cobol_runner import (
            executar_placa_original, executar_placa_convertido,
            comparar_placa, is_gnucobol_available
        )

        if not is_gnucobol_available():
            # Fallback para simulacao Python
            from executor_cobol import ValidadorPlaca
            validador = ValidadorPlaca()
            resultado = validador.validar(placa)
            return jsonify({
                "placa": resultado.placa,
                "valida": resultado.valida,
                "codigo": resultado.codigo,
                "descricao": resultado.descricao,
                "motor": "Python (simulacao - GnuCOBOL indisponivel)",
            })

        if fluxo == "original":
            res = executar_placa_original(placa)
            return jsonify({
                "placa": placa,
                "valida": res.codigo > 0,
                "codigo": res.codigo,
                "descricao": res.descricao,
                "motor": "GnuCOBOL - Original (PF-GAA-L004)",
                "tempo_ms": res.tempo_ms,
            })
        elif fluxo == "convertido":
            res = executar_placa_convertido(placa)
            return jsonify({
                "placa": placa,
                "valida": res.codigo > 0,
                "codigo": res.codigo,
                "descricao": res.descricao,
                "motor": "GnuCOBOL - Convertido (FGAA004)",
                "tempo_ms": res.tempo_ms,
            })
        else:
            # Comparar ambos
            comp = comparar_placa(placa)
            return jsonify({
                "placa": placa,
                "original": {
                    "codigo": comp.resultado_original.codigo,
                    "descricao": comp.resultado_original.descricao,
                    "tempo_ms": comp.resultado_original.tempo_ms,
                },
                "convertido": {
                    "codigo": comp.resultado_convertido.codigo,
                    "descricao": comp.resultado_convertido.descricao,
                    "tempo_ms": comp.resultado_convertido.tempo_ms,
                },
                "resultados_iguais": comp.resultados_iguais,
                "diferencas": comp.diferencas,
                "motor": "GnuCOBOL 3.1.2 (comparacao dual)",
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas gerais"""
    codigo_dir = Path(__file__).parent
    arquivos = list(codigo_dir.glob('TEST_RESULTS_*.json'))

    total_tests = 0
    total_passed = 0

    for arquivo in arquivos:
        try:
            with open(arquivo) as f:
                data = json.load(f)
                total_tests += data.get('total', 0)
                total_passed += data.get('passed', 0)
        except:
            pass

    taxa_sucesso = (total_passed / total_tests * 100) if total_tests > 0 else 0

    return jsonify({
        "total_execucoes": len(arquivos),
        "total_testes": total_tests,
        "total_passed": total_passed,
        "taxa_sucesso": taxa_sucesso,
    })

# Cache em memoria da estrutura gerada (evita recalcular a cada acesso).
# Os fontes nao mudam entre requisicoes, entao guardamos o resultado.
_estrutura_cache = {}


@app.route('/api/estrutura/gerar', methods=['POST'])
def gerar_estrutura():
    """Gera DDL + massa de dados a partir dos programas COBOL + copybooks.

    Usa a ferramenta tooling/ para inferir a estrutura das tabelas DB2 a partir
    dos EXEC SQL dos programas, tipando as colunas pelos copybooks disponiveis.
    O resultado e cacheado em memoria; envie {"forcar": true} para regerar.
    """
    try:
        data = request.json or {}
        n_massa = int(data.get('massa', 10))
        if n_massa < 1:
            n_massa = 1
        if n_massa > 50:
            n_massa = 50
        forcar = bool(data.get('forcar', False))

        # cache por quantidade de massa; retorna imediatamente se ja calculado
        chave = f'massa_{n_massa}'
        if not forcar and chave in _estrutura_cache:
            return jsonify(_estrutura_cache[chave])

        from tooling.orchestrator import gerar_para_web

        # Pastas de copybooks disponiveis (stubs + copybooks de tela entregues)
        pastas_copy = ['cobol_build/copy']
        amostra = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Originais')
        if amostra.exists():
            pastas_copy.append(str(amostra))

        resultado = gerar_para_web(
            'fontes_convertidos/Convertidos',
            pastas_copy,
            n_massa=n_massa,
        )
        _estrutura_cache[chave] = resultado
        return jsonify(resultado)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/estrutura/gerar-banco', methods=['POST'])
def gerar_banco_endpoint():
    """Gera a estrutura, cria o banco SQLite local e popula com massa de teste."""
    try:
        data = request.json or {}
        n_massa = int(data.get('massa', 10))
        n_massa = max(1, min(n_massa, 50))

        from tooling.orchestrator import gerar_banco_local

        pastas_copy = ['cobol_build/copy']
        amostra = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Originais')
        if amostra.exists():
            pastas_copy.append(str(amostra))

        resultado = gerar_banco_local(
            'fontes_convertidos/Convertidos',
            pastas_copy,
            db_path='saida_estrutura/prodesp_teste.db',
            n_massa=n_massa,
        )
        return jsonify(resultado)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/estrutura/tabela/<tabela>', methods=['GET'])
def get_registros_tabela(tabela):
    """Retorna a estrutura (coluna -> tipo/PIC/origem) e os registros de
    teste de uma tabela do banco SQLite (para o modal)."""
    try:
        from tooling.orchestrator import ler_registros_tabela, gerar_banco_local, estrutura_colunas_tabela
        db = 'saida_estrutura/prodesp_teste.db'
        pastas_copy = ['cobol_build/copy']
        amostra = Path('entregas/copybook-Amostragem POC  - Fontes Convertidos/Originais')
        if amostra.exists():
            pastas_copy.append(str(amostra))
        # se o banco ainda nao foi materializado, gera agora
        if not Path(db).exists():
            gerar_banco_local('fontes_convertidos/Convertidos', pastas_copy, db_path=db, n_massa=10)
        resultado = ler_registros_tabela(db, tabela, limite=100)
        resultado['estrutura'] = estrutura_colunas_tabela(
            'fontes_convertidos/Convertidos', pastas_copy, tabela)['colunas']
        return jsonify(resultado)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/testar-roteiro/<programa>', methods=['GET'])
def testar_com_roteiro(programa):
    """Executa o programa (original e convertido) usando os dados de teste de
    cada cenario do roteiro de Primeiro Emplacamento, para validacao."""
    try:
        from data.roteiros_teste import get_roteiros
        from cobol_runner import comparar_placa, executar_original, executar_convertido
        from data.program_mapping import get_converted_name

        is_placa = ('L004' in programa.upper() or programa.upper() == 'FGAA004'
                    or 'PF-GAA-L004' in programa.upper())

        casos = []
        for rot in get_roteiros():
            dt = rot.get('dados_teste', {})
            # entrada de teste: para validador de placa nao ha placa no roteiro (usa chassi
            # apenas como identificador); para os demais, usamos o chassi como entrada.
            entrada = dt.get('chassi', '')
            ident = dt.get('cpf') or dt.get('cnpj') or ''

            caso = {
                'cenario': rot['cenario'],
                'categoria': rot['categoria'],
                'chassi': dt.get('chassi', ''),
                'identificador': ident,
                'entrada': entrada,
                'passos': rot.get('passos', []),
            }

            try:
                if is_placa:
                    # o validador de placa espera uma placa; o roteiro nao tem placa,
                    # entao rodamos com o chassi so para exercitar (resultado indicativo)
                    comp = comparar_placa(entrada[:7] if entrada else '')
                    caso['original'] = {
                        'codigo': comp.resultado_original.codigo if comp.resultado_original else None,
                        'descricao': comp.resultado_original.descricao if comp.resultado_original else '',
                        'sucesso': bool(comp.resultado_original and comp.resultado_original.sucesso),
                    }
                    caso['convertido'] = {
                        'codigo': comp.resultado_convertido.codigo if comp.resultado_convertido else None,
                        'descricao': comp.resultado_convertido.descricao if comp.resultado_convertido else '',
                        'sucesso': bool(comp.resultado_convertido and comp.resultado_convertido.sucesso),
                    }
                    caso['iguais'] = comp.resultados_iguais
                else:
                    env = {'COB_PLACA': entrada, 'COB_CHASSI': entrada}
                    if dt.get('cpf'):
                        env['COB_CPF'] = dt['cpf']
                    if dt.get('cnpj'):
                        env['COB_CNPJ'] = dt['cnpj']
                    ro = executar_original(programa, env)
                    nome_conv = get_converted_name(programa) or programa
                    rc = executar_convertido(nome_conv, env)
                    caso['original'] = {'codigo': ro.codigo, 'descricao': ro.descricao or ro.output,
                                        'sucesso': ro.sucesso, 'erro': ro.erro}
                    caso['convertido'] = {'codigo': rc.codigo, 'descricao': rc.descricao or rc.output,
                                          'sucesso': rc.sucesso, 'erro': rc.erro}
                    caso['iguais'] = (ro.output == rc.output) and ro.sucesso and rc.sucesso
            except Exception as ex:
                caso['erro'] = str(ex)

            casos.append(caso)

        return jsonify({'programa': programa, 'is_placa': is_placa, 'casos': casos})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/roteiros', methods=['GET'])
def get_roteiros_endpoint():
    """Retorna os roteiros de teste de Primeiro Emplacamento (dos .docx)."""
    try:
        from data.roteiros_teste import get_roteiros, get_transacoes
        # indice de imagens (prints de tela) publicadas em static/roteiros/
        imagens = {}
        idx = Path('frontend/static/roteiros/indice.json')
        if idx.exists():
            imagens = json.loads(idx.read_text(encoding='utf-8'))
        return jsonify({
            'roteiros': get_roteiros(),
            'transacoes': get_transacoes(),
            'imagens': imagens,
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


HISTORICO_ROTEIRO_PATH = Path(__file__).resolve().parent / 'data' / 'roteiro_historico.json'
HISTORICO_ROTEIRO_MAX = 3


@app.route('/api/roteiro-historico', methods=['GET'])
def get_roteiro_historico():
    """Retorna as ultimas execucoes salvas do roteiro de testes (ate 3)."""
    try:
        historico = []
        if HISTORICO_ROTEIRO_PATH.exists():
            historico = json.loads(HISTORICO_ROTEIRO_PATH.read_text(encoding='utf-8'))
        return jsonify({'historico': historico})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/roteiro-historico', methods=['POST'])
def salvar_roteiro_historico():
    """Salva o resultado de uma execucao do roteiro de testes, mantendo
    apenas as ultimas HISTORICO_ROTEIRO_MAX - permite reabrir o relatorio
    (e baixar o PDF) de execucoes anteriores sem rodar tudo de novo."""
    try:
        dados = request.get_json(force=True) or {}
        resultados = dados.get('resultados')
        if not isinstance(resultados, list):
            return jsonify({"error": "campo 'resultados' (lista) e obrigatorio"}), 400

        entrada = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'quando': datetime.now().isoformat(timespec='seconds'),
            'alvo': dados.get('alvo', ''),
            'usuario': (session.get('user') or {}).get('username', ''),
            'resultados': resultados,
        }

        historico = []
        if HISTORICO_ROTEIRO_PATH.exists():
            try:
                historico = json.loads(HISTORICO_ROTEIRO_PATH.read_text(encoding='utf-8'))
            except Exception:
                historico = []

        historico.insert(0, entrada)
        historico = historico[:HISTORICO_ROTEIRO_MAX]
        HISTORICO_ROTEIRO_PATH.parent.mkdir(parents=True, exist_ok=True)
        HISTORICO_ROTEIRO_PATH.write_text(
            json.dumps(historico, ensure_ascii=False, indent=2), encoding='utf-8')
        return jsonify({'ok': True, 'total': len(historico)})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def _execute_tests():
    """Executa suite de testes em background"""
    global test_state

    # Suprimir saída de console durante testes
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        suite = TestSuite()

        # Executar testes
        test_state["current_test"] = "Iniciando testes..."
        test_state["progress"] = 10
        time.sleep(0.1)

        relatorio = suite.executar_todos()

        test_state["progress"] = 90

        # Salvar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = f"TEST_RESULTS_{timestamp}.json"
        with open(arquivo, "w") as f:
            json.dump(relatorio, f, indent=2)

        test_state["results"] = relatorio
        test_state["progress"] = 100
        test_state["current_test"] = None
        test_state["error"] = None

    except Exception as e:
        test_state["error"] = str(e)
        test_state["progress"] = -1
        test_state["current_test"] = None
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        test_state["running"] = False

def _execute_tests_expanded():
    """Executa suite de testes expandida em background"""
    global test_state

    # Suprimir saída de console durante testes
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        suite = TestSuiteExpanded()

        # Executar testes
        test_state["current_test"] = "Iniciando testes expandidos..."
        test_state["progress"] = 10
        time.sleep(0.1)

        relatorio = suite.executar_todos()

        test_state["progress"] = 90

        # Salvar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = f"TEST_RESULTS_EXPANDED_{timestamp}.json"
        with open(arquivo, "w") as f:
            json.dump(relatorio, f, indent=2)

        test_state["results"] = relatorio
        test_state["progress"] = 100
        test_state["current_test"] = None
        test_state["error"] = None

    except Exception as e:
        test_state["error"] = str(e)
        test_state["progress"] = -1
        test_state["current_test"] = None
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        test_state["running"] = False

def _execute_tests_custom(programas_selecionados):
    """Executa testes customizados (programas selecionados) em background"""
    global test_state

    # Suprimir saída de console durante testes
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        suite = TestSuiteExpanded(programas_selecionados=programas_selecionados)

        # Executar testes
        test_state["current_test"] = f"Testando {len(programas_selecionados)} programas..."
        test_state["progress"] = 10
        time.sleep(0.1)

        relatorio = suite.executar_todos()

        test_state["progress"] = 90

        # Salvar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = f"TEST_RESULTS_CUSTOM_{timestamp}.json"
        with open(arquivo, "w") as f:
            json.dump(relatorio, f, indent=2)

        test_state["results"] = relatorio
        test_state["progress"] = 100
        test_state["current_test"] = None
        test_state["error"] = None

    except Exception as e:
        test_state["error"] = str(e)
        test_state["progress"] = -1
        test_state["current_test"] = None
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        test_state["running"] = False

# =============================================================================
# FLUXO: LIMPAR PROJETO / IMPORTAR FONTES COBOL
# =============================================================================

def _limpar_artefatos_build():
    """Remove artefatos compilados em cobol_build, preservando os stubs em copy/."""
    from cobol_runner import BUILD_DIR
    removidos = 0
    if not BUILD_DIR.exists():
        return removidos
    padroes = ["*.dll", "*.so", "*_processed", "DRIVER-*.cob",
               "DRIVER-*.exe", "*.cob", "*.exe", "errors.txt"]
    for padrao in padroes:
        for f in BUILD_DIR.glob(padrao):
            if f.is_file():
                try:
                    f.unlink()
                    removidos += 1
                except Exception:
                    pass
    return removidos


@app.route('/api/projeto/limpar', methods=['POST'])
def limpar_projeto():
    """Limpa TODO o projeto, deixando-o pronto para importar fontes novos:

      - fontes de runtime: Originais (.C74/.cob, preserva copybooks MAPA_*.cpy)
        e Convertidos (todos os arquivos)
      - conteudo de 'arquivosimportados' (os fontes importados)
      - artefatos compilados em cobol_build (.dll/.so/.exe, DRIVER-*, *_processed,
        errors.txt) - preserva os stubs em cobol_build/copy
      - a estrutura/banco gerado em saida_estrutura (SQLite + DDL + massa)
      - o cache de estrutura em memoria
      - zera o registro de programas (a lista fica vazia ate reimportar)
    """
    global _estrutura_cache

    # Nao deixa limpar com uma importacao rodando: ela continuaria escrevendo
    # arquivos no thread em background por cima de um projeto recem-limpo,
    # deixando disco e o estado da importacao dessincronizados um do outro.
    if import_state["running"]:
        return jsonify({"ok": False, "error": (
            "Ha uma importacao em andamento - cancele-a "
            "(POST /api/projeto/importar/cancelar) ou aguarde terminar antes de limpar."
        )}), 409

    try:
        from cobol_runner import PROJECT_ROOT, ORIGINAIS_DIR, CONVERTIDOS_DIR
        from data.program_registry import salvar_mapa

        relatorio = {"originais_removidos": 0, "convertidos_removidos": 0,
                     "importados_removidos": 0, "artefatos_removidos": 0,
                     "estrutura_removida": False}

        # 1. Fontes originais (.C74/.cob), preservando copybooks MAPA_*.cpy
        if ORIGINAIS_DIR.exists():
            for f in ORIGINAIS_DIR.iterdir():
                if f.is_file() and f.suffix.lower() in ('.c74', '.cob') \
                        and not f.name.upper().startswith('MAPA_'):
                    try:
                        f.unlink()
                        relatorio["originais_removidos"] += 1
                    except Exception:
                        pass

        # 2. Fontes convertidos (arquivos sem extensao)
        if CONVERTIDOS_DIR.exists():
            for f in CONVERTIDOS_DIR.iterdir():
                if f.is_file():
                    try:
                        f.unlink()
                        relatorio["convertidos_removidos"] += 1
                    except Exception:
                        pass

        # 3. Diretorio de arquivos importados
        importados_dir = PROJECT_ROOT / 'arquivosimportados'
        if importados_dir.exists():
            for f in importados_dir.iterdir():
                if f.is_file():
                    try:
                        f.unlink()
                        relatorio["importados_removidos"] += 1
                    except Exception:
                        pass

        # 4. Artefatos compilados (preserva cobol_build/copy)
        relatorio["artefatos_removidos"] = _limpar_artefatos_build()

        # 5. Estrutura/banco gerado
        saida = PROJECT_ROOT / 'saida_estrutura'
        if saida.exists():
            import shutil
            try:
                shutil.rmtree(saida)
                relatorio["estrutura_removida"] = True
            except Exception:
                pass

        # 6. Cache em memoria e registro de programas
        _estrutura_cache = {}
        salvar_mapa({})

        return jsonify({"ok": True, "relatorio": relatorio})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


def _validar_cobol(conteudo: str, eh_copybook: bool):
    """Valida se o conteudo textual parece um fonte COBOL.

    Retorna (valido: bool, motivo: str). Aceita tanto programas completos
    (IDENTIFICATION/PROGRAM-ID/divisoes) quanto copybooks/mapas de tela (que
    sao apenas estrutura de dados: niveis 01/05/07 + PICTURE/PIC/REDEFINES/OCCURS).
    A validacao de estrutura de dados vale para qualquer arquivo - inclusive os
    auxiliares convertidos sem extensao (ex: AUML01, CCCC99, MENS01).
    """
    import re
    u = (conteudo or '').upper()

    # 1. Programa COBOL: divisoes / PROGRAM-ID
    # regex (nao substring de espaco unico): o formato fixo destes fontes usa
    # varios espacos entre palavras-chave (ex: "PROCEDURE   DIVISION.").
    tem_id = (re.search(r'IDENTIFICATION\s+DIVISION', u) is not None) or ('PROGRAM-ID' in u)
    tem_divisao = any(re.search(dv, u) for dv in (
        r'DATA\s+DIVISION', r'PROCEDURE\s+DIVISION',
        r'ENVIRONMENT\s+DIVISION', r'WORKING-STORAGE\s+SECTION',
    ))
    if tem_id and tem_divisao:
        return True, 'Programa COBOL valido'
    if tem_id or tem_divisao:
        return True, 'Fonte COBOL valido'

    # 2. Copybook / mapa de tela: estrutura de dados COBOL tipica.
    #    Vale para qualquer arquivo, nao so .cpy (os auxiliares convertidos
    #    vem sem extensao mas sao copybooks de tela).
    tem_nivel = re.search(r'(?m)^\s*\d{2}\s+[\w\-]+', u) is not None
    tem_pic = ('PIC ' in u) or ('PIC(' in u) or ('PICTURE' in u)
    tem_clausulas = any(c in u for c in ('OCCURS', 'REDEFINES', 'VALUE ', 'COMP', 'FILLER'))
    if tem_nivel and (tem_pic or tem_clausulas):
        return True, 'Copybook/estrutura COBOL valido'

    if eh_copybook:
        return False, 'Nao parece um copybook COBOL (sem niveis/PIC)'
    return False, 'Nao contem estruturas COBOL (DIVISION/PROGRAM-ID ou niveis/PIC)'


# Estado da importacao em andamento (pipeline com progresso por arquivo,
# no mesmo padrao de test_state: thread em background + polling de status).
import_state = {
    "running": False,
    "run_id": 0,            # identifica a execucao atual; uma thread antiga
                             # (travada, ou orfa de um reload) para de escrever
                             # no estado assim que ver que seu run_id ficou
                             # obsoleto - evita corromper uma importacao nova.
    "total": 0,
    "indice_atual": 0,      # 1-based: arquivo que esta sendo processado agora
    "arquivo_atual": None,
    "etapa_atual": None,    # 'validando' | 'gravando' | 'compilando' | None
    "etapa_iniciada_em": None,  # time.time() de quando a etapa atual comecou (rampa 0-100 continua)
    "compilacao_progresso": None,  # {iteracao, limite_iteracoes, elapsed, orcamento_segundos, simbolos_novos, simbolos_total}
    "nomes": [],            # nomes de todos os arquivos do lote, na ordem (pendentes + em curso + concluidos)
    "itens": [],            # [{arquivo, tipo, status, motivo, compilou, mensagem_compilacao}]
    "concluido": False,
    "erro": None,
    "resumo": None,
}


def _processar_importacao(pendentes, run_id):
    """Roda em thread separada: valida, grava e (se convertido) compila cada
    arquivo, atualizando import_state a cada etapa para o frontend acompanhar
    o pipeline em tempo real via polling.

    'run_id' identifica esta execucao - se import_state["run_id"] mudar (uma
    nova importacao foi iniciada, ou esta foi cancelada), a thread para de
    escrever no estado global e encerra, mesmo que ainda esteja no meio de
    um arquivo. Sem isso, uma thread presa (compilando um fonte grande) podia
    sobreviver a um cancelamento/reload e corromper o estado de uma execucao
    posterior.
    """
    global import_state
    try:
        from cobol_runner import ORIGINAIS_DIR, CONVERTIDOS_DIR, PROJECT_ROOT, compilar_modulo
        from data.program_registry import reconstruir_mapa_do_disco

        ORIGINAIS_DIR.mkdir(parents=True, exist_ok=True)
        CONVERTIDOS_DIR.mkdir(parents=True, exist_ok=True)
        IMPORTADOS_DIR = PROJECT_ROOT / 'arquivosimportados'
        IMPORTADOS_DIR.mkdir(parents=True, exist_ok=True)

        for idx, (nome, raw) in enumerate(pendentes, start=1):
            if import_state["run_id"] != run_id:
                return  # cancelada ou substituida por uma importacao mais nova
            import_state["indice_atual"] = idx
            import_state["arquivo_atual"] = nome
            import_state["etapa_atual"] = "validando"
            import_state["etapa_iniciada_em"] = time.time()
            import_state["compilacao_progresso"] = None

            item = {"arquivo": nome, "tipo": None, "status": None, "motivo": None,
                     "compilou": None, "mensagem_compilacao": None}

            if b'\x00' in raw:
                item["status"] = "rejeitado"
                item["motivo"] = "Arquivo binario (nao e texto COBOL)"
                import_state["itens"].append(item)
                continue

            try:
                conteudo = raw.decode('latin-1')
            except Exception:
                item["status"] = "rejeitado"
                item["motivo"] = "Nao foi possivel decodificar como texto"
                import_state["itens"].append(item)
                continue

            if not conteudo.strip():
                item["status"] = "rejeitado"
                item["motivo"] = "Arquivo vazio"
                import_state["itens"].append(item)
                continue

            ext = Path(nome).suffix.lower()
            eh_copybook = (ext == '.cpy')
            valido, motivo = _validar_cobol(conteudo, eh_copybook)
            item["motivo"] = motivo
            if not valido:
                item["status"] = "rejeitado"
                import_state["itens"].append(item)
                continue

            if ext in ('.c74', '.cob', '.cpy'):
                destino = ORIGINAIS_DIR / nome
                tipo = 'copybook' if eh_copybook else 'original'
            else:
                destino = CONVERTIDOS_DIR / nome
                tipo = 'convertido'
            item["tipo"] = tipo

            import_state["etapa_atual"] = "gravando"
            import_state["etapa_iniciada_em"] = time.time()
            try:
                destino.write_bytes(raw)
                try:
                    (IMPORTADOS_DIR / nome).write_bytes(raw)
                except Exception:
                    pass  # copia de backup nao deve falhar a importacao
            except Exception as e:
                item["status"] = "rejeitado"
                item["motivo"] = f"Erro ao gravar: {e}"
                import_state["itens"].append(item)
                continue

            item["status"] = "importado"

            # Fonte convertido (programa, nao copybook/original): compila ja
            # com o auto-inferidor, para ficar pronto para teste sem passo
            # manual extra (pode demorar bastante em fontes grandes).
            #
            # So tenta compilar quando o fonte tem PROCEDURE DIVISION: varios
            # "convertidos" sem extensao sao na verdade copybooks/mapas de
            # tela (ex: AUML01, CAPA01, MENS01) que o proprio _validar_cobol
            # ja identifica como estrutura de dados, nao programa executavel -
            # tentar compila-los sozinhos sempre falha (faltam DIVISIONs) e so
            # gera ruido de "nao compila" enganoso.
            # regex (nao substring simples): o formato fixo destes fontes usa
            # varios espacos entre palavras-chave (ex: "PROCEDURE   DIVISION."),
            # entao 'PROCEDURE DIVISION' in texto (espaco unico) falha e
            # marcava programas REAIS (FGAA004 etc.) como copybook por engano.
            import re as _re
            if tipo == 'convertido' and _re.search(r'PROCEDURE\s+DIVISION', conteudo.upper()):
                import_state["etapa_atual"] = "compilando"
                import_state["etapa_iniciada_em"] = time.time()

                def _reportar_progresso(info, _item=item):
                    # atualiza o estado global para o polling do front pegar;
                    # nunca deixa o progresso (so informativo) derrubar a compilacao
                    import_state["compilacao_progresso"] = info

                try:
                    ok_compila, msg_compila, _dll = compilar_modulo(nome, on_progress=_reportar_progresso)
                    item["compilou"] = ok_compila
                    item["mensagem_compilacao"] = msg_compila
                except Exception as e:
                    item["compilou"] = False
                    item["mensagem_compilacao"] = f"Erro ao compilar: {e}"
                finally:
                    import_state["compilacao_progresso"] = None
            elif tipo == 'convertido':
                item["mensagem_compilacao"] = "Copybook/estrutura (sem PROCEDURE DIVISION) - nao compilavel isoladamente"

            if import_state["run_id"] != run_id:
                return  # cancelada/substituida enquanto este arquivo compilava
            import_state["itens"].append(item)

        if import_state["run_id"] != run_id:
            return
        mapa = reconstruir_mapa_do_disco()
        itens = import_state["itens"]
        importados = [i for i in itens if i["status"] == "importado"]
        rejeitados = [i for i in itens if i["status"] == "rejeitado"]
        total_compilaveis = sum(1 for i in importados if i.get("tipo") == "convertido")
        total_compilaram = sum(1 for i in importados if i.get("compilou") is True)

        import_state["resumo"] = {
            "total_enviados": len(pendentes),
            "total_importados": len(importados),
            "total_rejeitados": len(rejeitados),
            "total_programas": len(mapa),
            "total_compilaveis": total_compilaveis,
            "total_compilaram": total_compilaram,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        if import_state["run_id"] == run_id:
            import_state["erro"] = str(e)
    finally:
        # so mexe no estado global se ainda for a execucao "dona" dele - uma
        # thread cancelada/substituida nao pode sobrescrever o running/
        # concluido de uma importacao mais nova que tenha assumido depois.
        if import_state["run_id"] == run_id:
            import_state["etapa_atual"] = None
            import_state["arquivo_atual"] = None
            import_state["running"] = False
            import_state["concluido"] = True


@app.route('/api/projeto/importar', methods=['POST'])
def importar_fontes():
    """Recebe os fontes COBOL via upload multipart e inicia a importacao em
    background (pipeline: validar -> gravar -> compilar por arquivo).

    Roteamento dos arquivos por extensao:
      - .C74 / .cob  -> fontes_convertidos/Originais
      - .cpy         -> fontes_convertidos/Originais (copybooks de mapa)
      - sem extensao -> fontes_convertidos/Convertidos (fonte convertido)

    O progresso (arquivo atual, etapa, resultados parciais) e consultado via
    GET /api/projeto/importar/status - o front faz polling para desenhar o
    pipeline passo a passo em vez de um spinner generico.
    """
    global import_state

    if import_state["running"]:
        return jsonify({"ok": False, "error": "Ja existe uma importacao em andamento"}), 409

    arquivos = request.files.getlist('arquivos')
    if not arquivos:
        return jsonify({"ok": False, "error": "Nenhum arquivo enviado"}), 400

    # Le o conteudo agora (dentro do contexto da requisicao) - o FileStorage
    # do Werkzeug nao sobrevive apos a thread em background assumir.
    pendentes = []
    for arq in arquivos:
        nome = os.path.basename(arq.filename or '').strip()
        if not nome:
            continue
        pendentes.append((nome, arq.read()))

    import_state["run_id"] += 1
    meu_run_id = import_state["run_id"]
    import_state["running"] = True
    import_state["total"] = len(pendentes)
    import_state["nomes"] = [nome for nome, _raw in pendentes]
    import_state["indice_atual"] = 0
    import_state["arquivo_atual"] = None
    import_state["etapa_atual"] = None
    import_state["compilacao_progresso"] = None
    import_state["itens"] = []
    import_state["concluido"] = False
    import_state["erro"] = None
    import_state["resumo"] = None

    thread = threading.Thread(target=_processar_importacao, args=(pendentes, meu_run_id))
    thread.daemon = True
    thread.start()

    return jsonify({"ok": True, "status": "iniciado", "total": len(pendentes)})


def _cancelar_import_ativo(motivo: str) -> bool:
    """Cancela a importacao em andamento (se houver). Retorna True se havia
    uma rodando e foi cancelada agora, False se nao havia nada para cancelar.

    Invalida o run_id atual: a thread em background ve a mudanca no proximo
    ponto de checagem (entre arquivos, ou logo apos compilar o atual) e para
    de escrever no estado, sem precisar matar a thread a forca. Libera a
    aplicacao para uma nova importacao ou para limpar o projeto.
    """
    if not import_state["running"]:
        return False
    import_state["run_id"] += 1  # invalida a thread atual
    import_state["running"] = False
    import_state["concluido"] = True
    import_state["etapa_atual"] = None
    import_state["arquivo_atual"] = None
    import_state["erro"] = motivo
    return True


@app.route('/api/projeto/importar/cancelar', methods=['POST'])
def cancelar_importacao():
    """Cancela a importacao em andamento (se houver), a pedido do usuario."""
    cancelou = _cancelar_import_ativo("Cancelado pelo usuario")
    return jsonify({"ok": True, "status": "cancelado" if cancelou else "nada_para_cancelar"})


def _percentual_etapa(etapa, compilacao_progresso, etapa_iniciada_em):
    """% (0-100) de progresso do arquivo em curso, como uma rampa continua -
    nao um salto fixo por etapa. 'validando' e 'gravando' sao quase
    instantaneos, entao rampam rapido dentro da sua faixa; 'compilando' e o
    unico que pode demorar de verdade, e usa o tempo decorrido (real, do
    auto-inferidor, ou estimado antes dele comecar a reportar) para avancar
    suavemente ate quase 100 em vez de ficar parado num numero fixo.
    """
    agora = time.time()
    decorrido_etapa = (agora - etapa_iniciada_em) if etapa_iniciada_em else 0

    if etapa == 'validando':
        # faixa 0-10%, rampa em ~0.3s (etapa e sub-segundo na pratica)
        return min(10, round(2 + 8 * min(1, decorrido_etapa / 0.3)))
    if etapa == 'gravando':
        # faixa 10-20%
        return min(20, round(12 + 8 * min(1, decorrido_etapa / 0.3)))
    if etapa == 'compilando':
        if compilacao_progresso and compilacao_progresso.get("orcamento_segundos"):
            # o auto-inferidor ja esta reportando tempo/orcamento real: usa
            # a fracao dele para preencher o resto da faixa (20-100%). Chega
            # a 100 de verdade perto do fim em vez de ficar preso em 98-99%
            # parecendo travado enquanto ainda esta processando.
            fracao = compilacao_progresso["elapsed"] / compilacao_progresso["orcamento_segundos"]
            return min(100, round(20 + 80 * fracao))
        # ainda na primeira tentativa de compilar (antes do auto-inferidor
        # entrar em acao, se precisar): rampa estimada assumindo ~8s tipicos
        # para essa primeira tentativa, sem nunca passar de 20%
        return min(20, round(2 + 18 * min(1, decorrido_etapa / 8)))
    return 0


@app.route('/api/projeto/importar/status', methods=['GET'])
def importar_status():
    """Status do pipeline de importacao em andamento (para polling)."""
    itens = import_state["itens"]
    nomes = import_state["nomes"]

    # progresso por arquivo (nome + %) para toda a lista do lote: concluidos
    # (100%), o atual (estimado pela etapa/tempo) e os ainda pendentes (0%) -
    # assim o usuario ve o pipeline inteiro, nao so o arquivo corrente.
    arquivos_progresso = []
    for i, nome in enumerate(nomes):
        if i < len(itens):
            it = itens[i]
            arquivos_progresso.append({
                "arquivo": nome, "percentual": 100, "status": it["status"],
                "compilou": it.get("compilou"),
            })
        elif nome == import_state["arquivo_atual"] and import_state["running"]:
            arquivos_progresso.append({
                "arquivo": nome,
                "percentual": _percentual_etapa(import_state["etapa_atual"], import_state["compilacao_progresso"],
                                                 import_state["etapa_iniciada_em"]),
                "status": "em_andamento", "compilou": None,
            })
        else:
            arquivos_progresso.append({"arquivo": nome, "percentual": 0, "status": "pendente", "compilou": None})

    return jsonify({
        "running": import_state["running"],
        "total": import_state["total"],
        "indice_atual": import_state["indice_atual"],
        "arquivo_atual": import_state["arquivo_atual"],
        "etapa_atual": import_state["etapa_atual"],
        "compilacao_progresso": import_state["compilacao_progresso"],
        "arquivos_progresso": arquivos_progresso,
        "itens": itens,
        "importados": [i for i in itens if i["status"] == "importado"],
        "rejeitados": [i for i in itens if i["status"] == "rejeitado"],
        "concluido": import_state["concluido"],
        "erro": import_state["erro"],
        "resumo": import_state["resumo"],
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
