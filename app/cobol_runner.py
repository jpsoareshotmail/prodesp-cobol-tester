"""
Executor real de programas COBOL via GnuCOBOL.
Suporta dois fluxos:
  - ORIGINAL: Fonte Micro Focus (.C74) adaptado para standalone (.cob)
  - CONVERTIDO: Fonte ja convertido, compilado como modulo (.dll) + driver

Estrutura de arquivos:
  fontes_convertidos/Originais/   -> fontes .C74 originais (Micro Focus)
  fontes_convertidos/Convertidos/ -> fontes convertidos (GnuCOBOL-ready)
  cobol_build/                    -> executaveis, drivers, dlls compilados
  cobol_build/copy/               -> copybooks stubs (WSGL, PDGL, etc)
"""
from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List

# Paths relativos ao projeto
import sys
import shutil

PROJECT_ROOT = Path(__file__).parent.parent
GNUCOBOL_DIR = PROJECT_ROOT / "gnucobol-bin" / "gnucobol-3.1.2-windows-mingw-x64"
COBOL_BIN = GNUCOBOL_DIR / "bin"
COBOL_CONFIG = GNUCOBOL_DIR / "share" / "gnucobol" / "config"
COBOL_COPY_SYSTEM = GNUCOBOL_DIR / "share" / "gnucobol" / "copy"
BUILD_DIR = PROJECT_ROOT / "cobol_build"

# Deteccao multiplataforma do compilador cobc:
#  - Windows: usa o GnuCOBOL empacotado no projeto (gnucobol-bin/.../cobc.exe)
#  - Linux/EC2: usa o cobc instalado no sistema (via 'dnf install gnucobol' etc.)
_IS_WINDOWS = sys.platform.startswith("win")
_COBC_WIN = COBOL_BIN / "cobc.exe"


def _resolver_cobc():
    """Descobre o caminho do compilador cobc conforme o SO/ambiente."""
    if _IS_WINDOWS and _COBC_WIN.exists():
        return str(_COBC_WIN)
    # Linux/macOS ou Windows sem o pacote local: procura no PATH do sistema
    sistema = shutil.which("cobc")
    if sistema:
        return sistema
    # fallback: retorna o caminho Windows (usado so para mensagens de status)
    return str(_COBC_WIN)


def _cobol_disponivel() -> bool:
    if _IS_WINDOWS and _COBC_WIN.exists():
        return True
    return shutil.which("cobc") is not None


# Extensoes dependentes de plataforma:
#  - executavel: '.exe' no Windows, '' no Linux
#  - modulo dinamico: '.dll' no Windows, '.so' no Linux
EXE_EXT = ".exe" if _IS_WINDOWS else ""
MOD_EXT = ".dll" if _IS_WINDOWS else ".so"
COPY_DIR = BUILD_DIR / "copy"
FONTES_DIR = PROJECT_ROOT / "fontes_convertidos"
ORIGINAIS_DIR = FONTES_DIR / "Originais"
CONVERTIDOS_DIR = FONTES_DIR / "Convertidos"

# Standalone sources (manually adapted for direct execution)
STANDALONE_DIR = BUILD_DIR


CODIGOS_PLACA = {
    0: "Invalida",
    11: "Mercosul - Sao Paulo",
    12: "Mercosul - Outros estados",
    21: "Antiga - Sao Paulo",
    22: "Antiga - Outros estados",
    33: "2 letras - Carros",
    34: "2 letras - Motos",
}


@dataclass
class ResultadoCOBOL:
    """Resultado generico de execucao COBOL."""
    programa: str
    fluxo: str  # "original" ou "convertido"
    sucesso: bool
    codigo: int = 0
    descricao: str = ""
    output: str = ""
    executado_cobol: bool = True
    erro: Optional[str] = None
    exe_path: Optional[str] = None
    fonte_path: Optional[str] = None
    tempo_ms: float = 0.0


@dataclass
class ResultadoComparacao:
    """Resultado de comparacao entre original e convertido."""
    programa_original: str
    programa_convertido: str
    resultado_original: Optional[ResultadoCOBOL] = None
    resultado_convertido: Optional[ResultadoCOBOL] = None
    resultados_iguais: bool = False
    diferencas: List[str] = field(default_factory=list)


def _get_env():
    """Retorna environment com PATH do GnuCOBOL configurado."""
    env = os.environ.copy()
    # COB_LIBRARY_PATH: onde o runtime procura os modulos (.dll/.so) - vale nos dois SOs
    env["COB_LIBRARY_PATH"] = str(BUILD_DIR)
    if _IS_WINDOWS and _COBC_WIN.exists():
        # GnuCOBOL empacotado (Windows): aponta PATH e dirs de config/copy do pacote
        env["PATH"] = str(COBOL_BIN) + os.pathsep + env.get("PATH", "")
        env["COB_CONFIG_DIR"] = str(COBOL_CONFIG)
        env["COB_COPY_DIR"] = str(COBOL_COPY_SYSTEM)
    # No Linux, o cobc do sistema ja conhece seus proprios diretorios de config/copy.
    return env


def _cobc():
    """Retorna caminho do compilador cobc (Windows empacotado ou sistema Linux)."""
    return _resolver_cobc()


_LARGER_REDEF_FLAG = None


def _flag_larger_redefines():
    """Retorna a flag correta para 'larger redefines' conforme a versao do cobc.
    - GnuCOBOL 3.1.x: -flarger-redefines-ok
    - GnuCOBOL 3.2.x: -flarger-redefines=ok
    Detecta uma vez consultando o --help do compilador.
    """
    global _LARGER_REDEF_FLAG
    if _LARGER_REDEF_FLAG is not None:
        return _LARGER_REDEF_FLAG
    try:
        result = subprocess.run([_cobc(), "--help"], capture_output=True, text=True, timeout=10)
        ajuda = (result.stdout or '') + (result.stderr or '')
        if '-flarger-redefines=' in ajuda:
            _LARGER_REDEF_FLAG = ["-flarger-redefines=ok"]      # 3.2+
        elif '-flarger-redefines-ok' in ajuda:
            _LARGER_REDEF_FLAG = ["-flarger-redefines-ok"]      # 3.1
        else:
            _LARGER_REDEF_FLAG = []                              # nao suportado -> omite
    except Exception:
        _LARGER_REDEF_FLAG = []
    return _LARGER_REDEF_FLAG


def _extrair_undefined(stderr: str) -> list:
    """Extrai nomes de variaveis/paragrafos 'not defined' do stderr do cobc."""
    import re
    matches = re.findall(r"'([^']+)' is not defined", stderr)
    # Filtrar apenas nomes validos COBOL (sem espacos, sem numeros puros)
    return [m for m in set(matches) if m[0].isalpha() and ' ' not in m]


def _adicionar_vars_ao_processed(source_path: Path, undefined: list):
    """Adiciona declaracoes para variaveis indefinidas no fonte processado."""
    content = source_path.read_text(encoding='latin-1')

    # Separar em variaveis (WS) e paragrafos (PD)
    ws_vars = []
    pd_paras = []
    for name in undefined:
        # Se tem HANDLE-, DATABASE- ou -DB2DMS = paragrafo
        if (name.startswith('HANDLE-') or name.startswith('DATABASE-') or
            '-DB2DMS' in name):
            pd_paras.append(name)
        else:
            # Tudo o resto (inclusive xxxDS) = variavel
            ws_vars.append(name)

    # Inserir variaveis antes de LINKAGE SECTION ou PROCEDURE DIVISION
    if ws_vars:
        var_block = '\n      * Auto-generated undefined vars\n'
        for v in sorted(ws_vars):
            vname = v[:30]
            var_block += f'       01  {vname:<30} PIC X(050) VALUE SPACES.\n'

        for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
            if marker in content:
                content = content.replace(marker, var_block + marker, 1)
                break

    # Inserir paragrafos antes do ultimo paragrafo (ou no final)
    if pd_paras:
        para_block = '\n      * Auto-generated undefined paragraphs\n'
        for p in sorted(pd_paras):
            para_block += f'       {p}.\n           CONTINUE.\n'

        # Inserir antes de COPY PDGL ou COPY PDGLDB ou ao final
        for marker in ['       COPY PDGL', '       COPY PDGLDB']:
            if marker in content:
                content = content.replace(marker, para_block + marker, 1)
                break
        else:
            content += '\n' + para_block

    source_path.write_text(content, encoding='latin-1')


def is_gnucobol_available() -> bool:
    """Verifica se o GnuCOBOL esta disponivel (Windows empacotado ou Linux sistema)."""
    return _cobol_disponivel()


# =============================================================================
# COMPILACAO
# =============================================================================

def compilar_standalone(nome: str) -> tuple:
    """
    Compila um programa standalone (.cob) em executavel (.exe).
    Usado para os fontes 'original' que foram adaptados manualmente.
    Retorna (sucesso, mensagem, path_exe).
    """
    source = STANDALONE_DIR / f"{nome}.cob"
    exe = BUILD_DIR / f"{nome}{EXE_EXT}"

    if not source.exists():
        # Verificar se existe o .C74 original (nao compilavel direto)
        orig_c74 = ORIGINAIS_DIR / f"{nome}.C74"
        if orig_c74.exists():
            return False, f"Fonte original disponivel apenas em formato Micro Focus (.C74). Adapte manualmente para .cob ou use o fluxo 'convertido'.", None
        return False, f"Fonte nao encontrado. Apenas PF-GAA-L004 possui versao standalone adaptada. Use o fluxo 'convertido' para testar este programa.", None

    if exe.exists() and exe.stat().st_mtime > source.stat().st_mtime:
        return True, "Cache (ja compilado)", str(exe)

    env = _get_env()
    try:
        result = subprocess.run(
            [_cobc(), "-x", "-free", str(source), "-o", str(exe)],
            capture_output=True, text=True, env=env, timeout=30,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0:
            return False, f"Erro compilacao: {result.stderr.strip()}", None
        return True, "Compilado", str(exe)
    except subprocess.TimeoutExpired:
        return False, "Timeout compilacao", None
    except FileNotFoundError:
        return False, "cobc nao encontrado", None
    except Exception as e:
        return False, str(e), None


def compilar_modulo(nome_convertido: str, on_progress=None) -> tuple:
    """
    Compila um fonte convertido como modulo (.dll).
    Se o fonte contiver EXEC SQL, pre-processa antes de compilar.
    Retorna (sucesso, mensagem, path_dll).

    'on_progress', se fornecido, e chamado a cada iteracao do auto-inferidor
    com um dict {iteracao, limite_iteracoes, elapsed, orcamento_segundos,
    simbolos_novos, simbolos_total} - usado pela UI para mostrar progresso
    real durante compilacoes longas em vez de um spinner parado.
    """
    source = CONVERTIDOS_DIR / nome_convertido
    dll = BUILD_DIR / f"{nome_convertido}{MOD_EXT}"

    if not source.exists():
        return False, f"Fonte convertido nao encontrado: {source}", None

    if dll.exists() and dll.stat().st_mtime > source.stat().st_mtime:
        return True, "Cache (ja compilado)", str(dll)

    # Pre-processar SQL se necessario
    from sql_preprocessor import preprocessar_arquivo
    processed_source = BUILD_DIR / f"{nome_convertido}_processed"
    ok, msg = preprocessar_arquivo(source, processed_source)
    if not ok:
        return False, f"Erro pre-processamento SQL: {msg}", None

    compile_source = processed_source if processed_source.exists() else source

    env = _get_env()

    def _compilar():
        return subprocess.run(
            [_cobc(), "-m", str(compile_source), "-o", str(dll),
             "-I", str(COPY_DIR), "-w", "-frelax-syntax-checks",
             "-frelax-level-hierarchy"] + _flag_larger_redefines(),
            capture_output=True, text=True, env=env, timeout=60,
            cwd=str(PROJECT_ROOT),
        )

    try:
        result = _compilar()
        if result.returncode == 0:
            return True, "Compilado como modulo", str(dll)

        # AUTO-INFERIDOR: tenta resolver simbolos ausentes gerando stubs
        # inferidos a partir do uso, e recompila. Loop com limite de iteracoes.
        try:
            from auto_inferidor import (
                extrair_undefined, extrair_qualificados, gerar_copybook_inferido,
                gerar_paragrafos_inferidos, injetar_copys,
            )
        except Exception:
            from app.auto_inferidor import (  # type: ignore
                extrair_undefined, extrair_qualificados, gerar_copybook_inferido,
                gerar_paragrafos_inferidos, injetar_copys,
            )

        codigo_proc = compile_source.read_text(encoding='latin-1', errors='ignore')
        vistos = set()
        qualificados_acumulado: dict = {}
        pares_vistos = set()  # (grupo, membro) ja incorporados ao .cpy
        # orcamento de tempo total (nao so numero de iteracoes): fontes muito
        # grandes tem cobc lento por chamada, e sem isso uma unica importacao
        # pode travar o pipeline por 10-15+ minutos num arquivo so.
        #
        # Proporcional ao tamanho do fonte: um arquivo pequeno que realmente
        # nao converge deve falhar rapido (nao vale a pena esperar 1500s por
        # todo mundo); ja um fonte gigante (ex: OGAA640D, 26 mil linhas) so
        # converge de verdade com bem mais tempo - dar o mesmo teto curto pra
        # ele so produz uma falha por timeout, nunca uma chance real.
        inicio = time.time()
        n_linhas = codigo_proc.count('\n') + 1
        ORCAMENTO_SEGUNDOS = max(240, min(3600, n_linhas // 10))
        LIMITE_ITERACOES = 60
        for iteracao in range(1, LIMITE_ITERACOES + 1):
            elapsed = time.time() - inicio
            if elapsed > ORCAMENTO_SEGUNDOS:
                return False, (f"Auto-inferencia excedeu {ORCAMENTO_SEGUNDOS}s "
                               f"(fonte grande demais para inferir automaticamente "
                               f"neste tempo) - ultimo erro: {result.stderr.strip()[:400]}"), None
            undefined = extrair_undefined(result.stderr)
            # so os que ainda nao tentamos declarar (evita loop infinito)
            novos = [u for u in undefined if u.upper() not in vistos]

            # acumula grupos qualificados (X IN/OF Y) tambem entre iteracoes.
            # Importante: um MESMO campo pode ser membro de grupos diferentes
            # (ex: TAX-VALOR IN DB02 e TAX-VALOR IN DB03 sao registros
            # distintos). Como extrair_undefined despe o qualificador, o nome
            # "puro" pode ja estar em vistos por causa de UM grupo enquanto a
            # associacao com OUTRO grupo ainda e nova - por isso o loop nao
            # pode parar so por causa de "novos" vazio; tambem precisa checar
            # se surgiu par (grupo, membro) inedito.
            for chave, info in extrair_qualificados(result.stderr).items():
                acc = qualificados_acumulado.setdefault(
                    chave, {"nome": info["nome"], "membros": set()})
                acc["membros"].update(info["membros"])
            pares_atuais = {(chave, m.upper()) for chave, info in qualificados_acumulado.items()
                            for m in info["membros"]}
            novos_pares = pares_atuais - pares_vistos

            if on_progress:
                try:
                    on_progress({
                        "iteracao": iteracao,
                        "limite_iteracoes": LIMITE_ITERACOES,
                        "elapsed": round(elapsed, 1),
                        "orcamento_segundos": ORCAMENTO_SEGUNDOS,
                        "simbolos_novos": len(novos) + len(novos_pares),
                        "simbolos_total": len(vistos) + len(novos),
                    })
                except Exception:
                    pass  # progresso e so informativo, nao pode derrubar a compilacao

            if not novos and not novos_pares:
                break
            vistos.update(u.upper() for u in novos)
            pares_vistos |= novos_pares

            # gerar_copybook_inferido/_paragrafos_inferidos SOBRESCREVEM o
            # .cpy a cada chamada; passar so "novos" perderia os simbolos
            # ja resolvidos em iteracoes anteriores. Passa o acumulado.
            _cpy, resumo = gerar_copybook_inferido(
                nome_convertido, sorted(vistos), codigo_proc, COPY_DIR,
                qualificados=qualificados_acumulado)
            gerar_paragrafos_inferidos(nome_convertido, resumo["paragrafos"], COPY_DIR)
            injetar_copys(
                compile_source, nome_convertido,
                tem_dados=bool(resumo["campos"]),
                tem_paragrafos=bool(resumo["paragrafos"]),
            )
            codigo_proc = compile_source.read_text(encoding='latin-1', errors='ignore')

            # remove o .dll antigo para nao pegar cache e recompila
            try:
                if dll.exists():
                    dll.unlink()
            except Exception:
                pass
            result = _compilar()
            if result.returncode == 0:
                return True, "Compilado (com simbolos inferidos)", str(dll)

        # ainda falhou: retorna o erro (agora com mais contexto)
        return False, f"Erro compilacao: {result.stderr.strip()[:600]}", None
    except subprocess.TimeoutExpired:
        return False, "Timeout compilacao", None
    except FileNotFoundError:
        return False, "cobc nao encontrado", None
    except Exception as e:
        return False, str(e), None


_TOKEN_TO_ENV = [
    # (fragmento no nome do campo, variavel de ambiente com o dado de teste)
    # ordem importa: checar CNPJ antes de CPF evita falso-positivo se algum
    # campo combinar os dois nomes.
    ('CNPJ', 'COB_CNPJ'),
    ('CPF', 'COB_CPF'),
    ('CHASS', 'COB_CHASSI'),
    ('PLACA', 'COB_PLACA'),
]
_FRAGMENTOS_SAIDA = ('RETORNO', 'RET', 'SIT', 'COD', 'STATUS', 'FLAG', 'BLQ')


def _extrair_using_params(content: str) -> list:
    """Extrai os nomes dos parametros de 'PROCEDURE DIVISION USING p1 p2.'.

    A clausula frequentemente quebra linha no formato fixo sem hifen de
    continuacao (ex: FGAA012D), por isso a busca e feita com DOTALL ate o
    primeiro ponto final.
    """
    m = re.search(r'(?i)PROCEDURE\s+DIVISION\s+USING\s+(.*?)\.', content, re.DOTALL)
    if not m:
        return []
    bruto = re.sub(r'(?i)\bBY\s+(REFERENCE|VALUE|CONTENT)\b', ' ', m.group(1))
    return re.findall(r'[A-Za-z][\w-]*', bruto)


def _extrair_bloco_linkage(content: str, nome_param: str) -> str | None:
    """Extrai o bloco '01 NOME_PARAM. ...' da LINKAGE SECTION, verbatim
    (preserva REDEFINES/OCCURS/colunas), ate o proximo '01' de topo ou
    PROCEDURE DIVISION."""
    linhas = content.split('\n')
    idx_linkage = next((i for i, ln in enumerate(linhas)
                         if re.match(r'(?i)^\s*LINKAGE\s+SECTION\b', ln)), None)
    if idx_linkage is None:
        return None
    tok = r'(?<![A-Za-z0-9-])' + re.escape(nome_param) + r'(?![A-Za-z0-9-])'
    idx_inicio = next((i for i in range(idx_linkage + 1, len(linhas))
                        if re.match(r'(?i)^\s*01\s+' + tok, linhas[i])), None)
    if idx_inicio is None:
        return None
    idx_fim = len(linhas)
    for i in range(idx_inicio + 1, len(linhas)):
        if re.match(r'(?i)^\s*01\s+[A-Za-z]', linhas[i]) or re.match(r'(?i)^\s*PROCEDURE\s+DIVISION', linhas[i]):
            idx_fim = i
            break
    return '\n'.join(linhas[idx_inicio:idx_fim]).rstrip()


def _extrair_campos_pic(bloco: str) -> list:
    """Lista (nivel, nome, pic) dos campos com PIC de um bloco LINKAGE,
    ignorando comentarios, FILLER, REDEFINES (aliases, nao alvos de MOVE)
    e 88-niveis (condition-names, sem PIC)."""
    campos = []
    for ln in bloco.split('\n'):
        if len(ln) >= 7 and ln[6] in ('*', '/'):
            continue
        if re.search(r'(?i)\bREDEFINES\b', ln):
            continue
        m = re.match(r'^\s*(\d\d)\s+([A-Za-z][\w-]*)\s+.*?PIC(?:TURE)?\s+(?:IS\s+)?([9XASV(),.\-]+)',
                     ln, re.IGNORECASE)
        if m and m.group(2).upper() != 'FILLER':
            campos.append((m.group(1), m.group(2), m.group(3)))
    return campos


def _gerar_driver_com_parametros(nome_convertido: str, content: str) -> str | None:
    """Gera um driver que passa dados REAIS de teste para programas com
    'PROCEDURE DIVISION USING ...' (a maioria dos programas nao segue o
    padrao LC-PARM/LC-PLACA de validador de placa, e sem isso o driver
    generico chamava o programa SEM nenhum parametro - o dado do roteiro
    nunca chegava dentro do programa, so' o RETURN-CODE (sempre 0) era
    exibido, fazendo todo programa "dar o mesmo resultado").

    Copia o(s) bloco(s) LINKAGE verbatim para WORKING-STORAGE (mesma tecnica
    ja usada no driver hardcoded de LC-PARM), preenche por heuristica de
    nome os campos de entrada reconhecidos (chassi/placa/cpf/cnpj, vindos
    de variaveis de ambiente) e, apos o CALL, exibe tambem um campo de
    retorno real do programa (heuristica por nome no bloco de saida) alem
    do RETURN-CODE - assim o resultado reflete a execucao de verdade.

    Retorna None (deixa o chamador cair no driver generico sem parametros)
    quando a estrutura foge do padrao observado (mais de 2 parametros,
    bloco LINKAGE nao encontrado, ou nenhum campo de entrada reconhecivel -
    nesse ultimo caso gerar um driver "as cegas" nao ajudaria).
    """
    params = _extrair_using_params(content)
    if not params or len(params) > 2:
        return None

    blocos = []
    for p in params:
        bloco = _extrair_bloco_linkage(content, p)
        if not bloco:
            return None
        blocos.append((p, bloco))

    # qual parametro e entrada e qual e saida: heuristica pelo nome (contem
    # RET) com fallback posicional (1o = entrada, 2o = saida), que e a
    # convencao observada em todos os programas reais (AX-LIB-*/AX-*-ENVL*
    # antes, AX-*-RET*/AX-RET-* depois).
    idx_saida = next((i for i, (nome, _) in enumerate(blocos) if 'RET' in nome.upper()), None)
    if idx_saida is None:
        idx_saida = len(blocos) - 1
    idx_entrada = 0 if idx_saida != 0 else (1 if len(blocos) > 1 else 0)

    campos_entrada = _extrair_campos_pic(blocos[idx_entrada][1])
    moves = []
    envs_usadas = []
    for _nivel, nome_campo, _pic in campos_entrada:
        for fragmento, envvar in _TOKEN_TO_ENV:
            if fragmento in nome_campo.upper():
                if envvar not in envs_usadas:
                    envs_usadas.append(envvar)
                moves.append((envvar, nome_campo))
                break
    if not moves:
        # nenhum campo reconhecivel para preencher - gerar um driver que so
        # chama sem dados nao teria vantagem sobre o generico
        return None

    campos_saida = _extrair_campos_pic(blocos[idx_saida][1]) if len(blocos) > 1 else campos_entrada
    campo_saida = None
    for fragmento in _FRAGMENTOS_SAIDA:
        campo_saida = next((nome for _n, nome, _p in campos_saida if fragmento in nome.upper()), None)
        if campo_saida:
            break

    linhas = [
        '       IDENTIFICATION DIVISION.',
        '       PROGRAM-ID. DRIVER-%s.' % nome_convertido,
        '',
        '       ENVIRONMENT DIVISION.',
        '       CONFIGURATION SECTION.',
        '       REPOSITORY.',
        '           FUNCTION ALL INTRINSIC.',
        '',
        '       DATA DIVISION.',
        '       WORKING-STORAGE SECTION.',
    ]
    for envvar in envs_usadas:
        campo_ws = 'WS-IN-' + envvar.replace('COB_', '')
        linhas.append('       01  %-30s PIC X(040).' % campo_ws)
    linhas.append('       01  WS-RETURN-CODE     PIC 9(004) VALUE 0.')
    for _nome, bloco in blocos:
        linhas.append(bloco)
    linhas.append('')
    linhas.append('       PROCEDURE DIVISION.')
    linhas.append('       MAIN-PARA.')
    for envvar in envs_usadas:
        campo_ws = 'WS-IN-' + envvar.replace('COB_', '')
        linhas.append('           ACCEPT %s FROM ENVIRONMENT "%s"' % (campo_ws, envvar))
    for envvar, nome_campo in moves:
        campo_ws = 'WS-IN-' + envvar.replace('COB_', '')
        linhas.append('           MOVE UPPER-CASE(%s) TO %s' % (campo_ws, nome_campo))
    nomes_params = [nome for nome, _ in blocos]
    linhas.append('           CALL "%s" USING %s' % (nome_convertido, nomes_params[0]))
    for extra in nomes_params[1:]:
        linhas.append('               %s' % extra)
    linhas.append('           MOVE RETURN-CODE TO WS-RETURN-CODE')
    linhas.append('           DISPLAY WS-RETURN-CODE')
    if campo_saida:
        linhas.append('           DISPLAY "RESULT=" %s' % campo_saida)
    linhas.append('           STOP RUN.')
    return '\n'.join(linhas) + '\n'


def _gerar_driver(nome_convertido: str, driver_path: Path):
    """
    Gera automaticamente um driver .cob para chamar o modulo convertido.
    Prioridade: (1) padrao LC-PARM/LC-PLACA hardcoded (validador de placa),
    (2) driver com parametros reais inferidos da LINKAGE SECTION para
    programas com PROCEDURE DIVISION USING, (3) driver generico sem
    parametros (programas CICS que recebem dado via canal/container, nao
    por CALL - continuam corretamente sem input aqui).
    """
    # Ler o fonte convertido para extrair a LINKAGE SECTION
    source = CONVERTIDOS_DIR / nome_convertido
    if not source.exists():
        return

    content = source.read_text(encoding='latin-1')

    # Verificar se tem LINKAGE com LC-PARM (padrao de placas)
    has_lc_parm = "LC-PARM" in content and "LC-PLACA" in content

    driver_code = None
    if not has_lc_parm:
        driver_code = _gerar_driver_com_parametros(nome_convertido, content)

    if has_lc_parm:
        # Driver para programas tipo validador de placa
        driver_code = f"""       IDENTIFICATION DIVISION.
       PROGRAM-ID. DRIVER-{nome_convertido}.

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       REPOSITORY.
           FUNCTION ALL INTRINSIC.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01  LC-PARM.
           05  LC-RETORNO              PIC 9(002).
           05  LC-PLACA                PIC X(010).
           05  LC-PLACA-R             REDEFINES LC-PLACA.
             10  LC-FAIXA.
               15  FILLER             PIC X(002).
               15  LC-FAIXA-3         PIC X(001).
             10  LC-MILHAR            PIC X(001).
             10  LC-SERIE             PIC X(001).
             10  LC-DEZENA            PIC X(002).
             10  FILLER               PIC X(003).

       01  WS-INPUT                   PIC X(010).

       PROCEDURE DIVISION.
       MAIN-PARA.
           ACCEPT WS-INPUT FROM ENVIRONMENT "COB_PLACA"
           MOVE UPPER-CASE(WS-INPUT) TO LC-PLACA
           MOVE 00 TO LC-RETORNO

           CALL "{nome_convertido}" USING LC-PARM

           DISPLAY LC-RETORNO
           STOP RUN.
"""
    elif driver_code is None:
        # Driver generico - apenas chama e exibe return code (programas sem
        # PROCEDURE DIVISION USING, ex: CICS que recebe dado por canal, ou
        # cuja LINKAGE nao tem campo de entrada reconhecivel)
        driver_code = f"""       IDENTIFICATION DIVISION.
       PROGRAM-ID. DRIVER-{nome_convertido}.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-RETURN-CODE     PIC 9(004) VALUE 0.

       PROCEDURE DIVISION.
       MAIN-PARA.
           CALL "{nome_convertido}"
           MOVE RETURN-CODE TO WS-RETURN-CODE
           DISPLAY WS-RETURN-CODE
           STOP RUN.
"""

    driver_path.write_text(driver_code, encoding='utf-8')


def compilar_driver(nome_convertido: str) -> tuple:
    """
    Compila o driver para chamar um modulo convertido.
    Se o driver .cob nao existir, gera automaticamente um driver generico.
    Retorna (sucesso, mensagem, path_exe).
    """
    driver_source = BUILD_DIR / f"DRIVER-{nome_convertido}.cob"
    driver_exe = BUILD_DIR / f"DRIVER-{nome_convertido}{EXE_EXT}"

    # Gerar driver automaticamente se nao existir
    if not driver_source.exists():
        _gerar_driver(nome_convertido, driver_source)

    if not driver_source.exists():
        return False, f"Nao foi possivel gerar driver para: {nome_convertido}", None

    if driver_exe.exists() and driver_exe.stat().st_mtime > driver_source.stat().st_mtime:
        return True, "Cache (ja compilado)", str(driver_exe)

    env = _get_env()
    try:
        result = subprocess.run(
            [_cobc(), "-x", str(driver_source), "-o", str(driver_exe),
             "-w", "-frelax-syntax-checks"] + _flag_larger_redefines(),
            capture_output=True, text=True, env=env, timeout=30,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0:
            return False, f"Erro compilacao driver: {result.stderr.strip()}", None
        return True, "Driver compilado", str(driver_exe)
    except subprocess.TimeoutExpired:
        return False, "Timeout compilacao driver", None
    except FileNotFoundError:
        return False, "cobc nao encontrado", None
    except Exception as e:
        return False, str(e), None


# =============================================================================
# EXECUCAO - FLUXO ORIGINAL
# =============================================================================

def _parsear_resultado_driver(output: str) -> tuple:
    """Extrai (codigo, descricao) da saida do driver.

    Layout: 1a linha sempre e o RETURN-CODE; quando o driver conseguiu
    identificar um campo de retorno real do programa (heuristica em
    _gerar_driver_com_parametros), uma 2a linha 'RESULT=<valor>' traz esse
    valor - e essa e a que importa para o teste (o RETURN-CODE sozinho quase
    sempre fica 0). Mantem compatibilidade com o layout antigo (so
    RETURN-CODE, sem RESULT=), usado pelo driver de placa e pelo generico.
    """
    linhas = [l.strip() for l in (output or '').split('\n') if l.strip()]
    if not linhas:
        return 0, ''
    resultado = next((l.split('=', 1)[1].strip() for l in linhas if l.upper().startswith('RESULT=')), None)
    alvo = resultado if resultado is not None else linhas[0]
    try:
        return int(alvo), ''
    except ValueError:
        return 0, alvo


def executar_original(programa: str, env_vars: Dict[str, str] = None) -> ResultadoCOBOL:
    """
    Executa o programa ORIGINAL (standalone .cob -> .exe).
    O programa deve ter sido adaptado para aceitar input via env vars.
    """
    import time
    start = time.time()

    nome_standalone = programa  # Ex: "PF-GAA-L004"
    sucesso, msg, exe_path = compilar_standalone(nome_standalone)

    if not sucesso:
        return ResultadoCOBOL(
            programa=programa, fluxo="original", sucesso=False,
            erro=msg, executado_cobol=False,
        )

    env = _get_env()
    if env_vars:
        env.update(env_vars)

    try:
        result = subprocess.run(
            [exe_path], capture_output=True, text=True,
            env=env, timeout=10, cwd=str(BUILD_DIR),
        )
        elapsed = (time.time() - start) * 1000
        output = result.stdout.strip()
        codigo, descricao = _parsear_resultado_driver(output)

        return ResultadoCOBOL(
            programa=programa, fluxo="original", sucesso=True,
            codigo=codigo, descricao=descricao,
            output=output, executado_cobol=True,
            exe_path=exe_path,
            fonte_path=str(STANDALONE_DIR / f"{nome_standalone}.cob"),
            tempo_ms=elapsed,
        )
    except subprocess.TimeoutExpired:
        return ResultadoCOBOL(
            programa=programa, fluxo="original", sucesso=False,
            erro="Timeout (>10s)", executado_cobol=False,
        )
    except Exception as e:
        return ResultadoCOBOL(
            programa=programa, fluxo="original", sucesso=False,
            erro=str(e), executado_cobol=False,
        )


# =============================================================================
# EXECUCAO - FLUXO CONVERTIDO
# =============================================================================

def executar_convertido(nome_convertido: str, env_vars: Dict[str, str] = None) -> ResultadoCOBOL:
    """
    Executa o programa CONVERTIDO (modulo .dll via driver .exe).
    """
    import time
    start = time.time()

    # Compilar modulo
    sucesso, msg, dll_path = compilar_modulo(nome_convertido)
    if not sucesso:
        return ResultadoCOBOL(
            programa=nome_convertido, fluxo="convertido", sucesso=False,
            erro=f"Modulo: {msg}", executado_cobol=False,
        )

    # Compilar driver
    sucesso, msg, driver_exe = compilar_driver(nome_convertido)
    if not sucesso:
        return ResultadoCOBOL(
            programa=nome_convertido, fluxo="convertido", sucesso=False,
            erro=f"Driver: {msg}", executado_cobol=False,
        )

    env = _get_env()
    if env_vars:
        env.update(env_vars)

    try:
        result = subprocess.run(
            [driver_exe], capture_output=True, text=True,
            env=env, timeout=10, cwd=str(BUILD_DIR),
        )
        elapsed = (time.time() - start) * 1000
        output = result.stdout.strip()
        codigo, descricao = _parsear_resultado_driver(output)

        return ResultadoCOBOL(
            programa=nome_convertido, fluxo="convertido", sucesso=True,
            codigo=codigo, descricao=descricao,
            output=output, executado_cobol=True,
            exe_path=driver_exe,
            fonte_path=str(CONVERTIDOS_DIR / nome_convertido),
            tempo_ms=elapsed,
        )
    except subprocess.TimeoutExpired:
        return ResultadoCOBOL(
            programa=nome_convertido, fluxo="convertido", sucesso=False,
            erro="Timeout (>10s)", executado_cobol=False,
        )
    except Exception as e:
        return ResultadoCOBOL(
            programa=nome_convertido, fluxo="convertido", sucesso=False,
            erro=str(e), executado_cobol=False,
        )


# =============================================================================
# FUNCOES ESPECIFICAS - PF-GAA-L004 / FGAA004 (Validador de Placas)
# =============================================================================

def executar_placa_original(placa: str) -> ResultadoCOBOL:
    """Executa validacao de placa com o programa ORIGINAL."""
    resultado = executar_original("PF-GAA-L004", {"COB_PLACA": placa.strip().upper() if placa else ""})
    if resultado.sucesso and resultado.output:
        try:
            codigo = int(resultado.output)
            resultado.codigo = codigo
            resultado.descricao = CODIGOS_PLACA.get(codigo, f"Codigo {codigo}")
        except ValueError:
            resultado.codigo = -1
            resultado.descricao = f"Retorno invalido: {resultado.output}"
    return resultado


def executar_placa_convertido(placa: str) -> ResultadoCOBOL:
    """Executa validacao de placa com o programa CONVERTIDO."""
    resultado = executar_convertido("FGAA004", {"COB_PLACA": placa.strip().upper() if placa else ""})
    if resultado.sucesso and resultado.output:
        try:
            codigo = int(resultado.output)
            resultado.codigo = codigo
            resultado.descricao = CODIGOS_PLACA.get(codigo, f"Codigo {codigo}")
        except ValueError:
            resultado.codigo = -1
            resultado.descricao = f"Retorno invalido: {resultado.output}"
    return resultado


def comparar_placa(placa: str) -> ResultadoComparacao:
    """Executa a mesma placa nos dois fluxos e compara resultados."""
    res_orig = executar_placa_original(placa)
    res_conv = executar_placa_convertido(placa)

    diferencas = []
    iguais = True

    if res_orig.codigo != res_conv.codigo:
        iguais = False
        diferencas.append(
            f"Codigo: original={res_orig.codigo} ({res_orig.descricao}) "
            f"vs convertido={res_conv.codigo} ({res_conv.descricao})"
        )

    if res_orig.output != res_conv.output:
        iguais = False
        diferencas.append(
            f"Output: original='{res_orig.output}' vs convertido='{res_conv.output}'"
        )

    return ResultadoComparacao(
        programa_original="PF-GAA-L004",
        programa_convertido="FGAA004",
        resultado_original=res_orig,
        resultado_convertido=res_conv,
        resultados_iguais=iguais,
        diferencas=diferencas,
    )


# =============================================================================
# INFORMACOES DE STATUS
# =============================================================================

def get_status() -> Dict:
    """Retorna status do ambiente COBOL."""
    cobc_path = _cobc()
    standalone_cob = STANDALONE_DIR / "PF-GAA-L004.cob"
    standalone_exe = BUILD_DIR / f"PF-GAA-L004{EXE_EXT}"
    convertido_src = CONVERTIDOS_DIR / "FGAA004"
    convertido_dll = BUILD_DIR / f"FGAA004{MOD_EXT}"
    driver_exe = BUILD_DIR / f"DRIVER-FGAA004{EXE_EXT}"

    return {
        "gnucobol_disponivel": _cobol_disponivel(),
        "compilador": cobc_path,
        "fontes_originais": str(ORIGINAIS_DIR),
        "fontes_convertidos": str(CONVERTIDOS_DIR),
        "build_dir": str(BUILD_DIR),
        "copybooks_dir": str(COPY_DIR),
        "original": {
            "fonte": str(standalone_cob),
            "fonte_existe": standalone_cob.exists(),
            "executavel": str(standalone_exe),
            "executavel_existe": standalone_exe.exists(),
        },
        "convertido": {
            "fonte": str(convertido_src),
            "fonte_existe": convertido_src.exists(),
            "modulo": str(convertido_dll),
            "modulo_existe": convertido_dll.exists(),
            "driver": str(driver_exe),
            "driver_existe": driver_exe.exists(),
        },
        "total_originais": len(list(ORIGINAIS_DIR.glob("PF-*"))) if ORIGINAIS_DIR.exists() else 0,
        "total_convertidos": len([f for f in CONVERTIDOS_DIR.iterdir() if f.is_file() and not f.name.startswith("MAPA")]) if CONVERTIDOS_DIR.exists() else 0,
    }
