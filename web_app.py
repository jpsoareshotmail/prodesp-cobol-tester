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

app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
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
    session['user'] = user
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
    """Retorna lista de programas com mapeamento original/convertido"""
    from data.program_mapping import get_programs_by_category, PROGRAM_MAP
    from cobol_runner import ORIGINAIS_DIR, CONVERTIDOS_DIR, BUILD_DIR

    resultado = {}
    for category, progs in get_programs_by_category().items():
        resultado[category] = []
        for prog in progs:
            orig_file = ORIGINAIS_DIR / prog["original_file"]
            conv_file = CONVERTIDOS_DIR / prog["converted_file"]
            standalone = BUILD_DIR / f"{prog['original']}.cob"
            driver = BUILD_DIR / f"DRIVER-{prog['converted']}.cob"
            resultado[category].append({
                "original": prog["original"],
                "convertido": prog["converted"],
                "original_existe": orig_file.exists(),
                "convertido_existe": conv_file.exists(),
                "standalone_pronto": standalone.exists(),
                "driver_pronto": driver.exists(),
            })

    return jsonify({
        "categorias": resultado,
        "total_programas": len(PROGRAM_MAP),
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

@app.route('/api/codigo-fonte/<programa>', methods=['GET'])
def get_codigo_fonte_dual(programa):
    """Retorna codigo fonte do programa em ambas versoes (original e convertido)"""
    from cobol_runner import ORIGINAIS_DIR, CONVERTIDOS_DIR
    from data.program_mapping import get_converted_name, get_original_name

    resultado = {"programa": programa, "original": None, "convertido": None}

    # Determinar nomes
    nome_convertido = get_converted_name(programa)
    nome_original = get_original_name(programa) if not nome_convertido else programa

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
            except:
                pass

    return jsonify(resultado)

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

@app.route('/api/estrutura/gerar', methods=['POST'])
def gerar_estrutura():
    """Gera DDL + massa de dados a partir dos programas COBOL + copybooks.

    Usa a ferramenta tooling/ para inferir a estrutura das tabelas DB2 a partir
    dos EXEC SQL dos programas, tipando as colunas pelos copybooks disponiveis.
    """
    try:
        data = request.json or {}
        n_massa = int(data.get('massa', 10))
        if n_massa < 1:
            n_massa = 1
        if n_massa > 50:
            n_massa = 50

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
        return jsonify(resultado)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/roteiros', methods=['GET'])
def get_roteiros_endpoint():
    """Retorna os roteiros de teste de Primeiro Emplacamento (dos .docx)."""
    try:
        from data.roteiros_teste import get_roteiros, get_transacoes
        return jsonify({
            'roteiros': get_roteiros(),
            'transacoes': get_transacoes(),
        })
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
