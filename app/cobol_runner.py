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

import os
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List

# Paths relativos ao projeto
PROJECT_ROOT = Path(__file__).parent.parent
GNUCOBOL_DIR = PROJECT_ROOT / "gnucobol-bin" / "gnucobol-3.1.2-windows-mingw-x64"
COBOL_BIN = GNUCOBOL_DIR / "bin"
COBOL_CONFIG = GNUCOBOL_DIR / "share" / "gnucobol" / "config"
COBOL_COPY_SYSTEM = GNUCOBOL_DIR / "share" / "gnucobol" / "copy"
BUILD_DIR = PROJECT_ROOT / "cobol_build"
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
    env["PATH"] = str(COBOL_BIN) + os.pathsep + env.get("PATH", "")
    env["COB_CONFIG_DIR"] = str(COBOL_CONFIG)
    env["COB_COPY_DIR"] = str(COBOL_COPY_SYSTEM)
    env["COB_LIBRARY_PATH"] = str(BUILD_DIR)
    return env


def _cobc():
    """Retorna caminho absoluto do compilador cobc."""
    return str(COBOL_BIN / "cobc.exe")


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
    """Verifica se o GnuCOBOL esta disponivel."""
    cobc = COBOL_BIN / "cobc.exe"
    return cobc.exists()


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
    exe = BUILD_DIR / f"{nome}.exe"

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


def compilar_modulo(nome_convertido: str) -> tuple:
    """
    Compila um fonte convertido como modulo (.dll).
    Se o fonte contiver EXEC SQL, pre-processa antes de compilar.
    Retorna (sucesso, mensagem, path_dll).
    """
    source = CONVERTIDOS_DIR / nome_convertido
    dll = BUILD_DIR / f"{nome_convertido}.dll"

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
    try:
        result = subprocess.run(
            [_cobc(), "-m", str(compile_source), "-o", str(dll),
             "-I", str(COPY_DIR), "-w", "-frelax-syntax-checks",
             "-frelax-level-hierarchy", "-flarger-redefines-ok"],
            capture_output=True, text=True, env=env, timeout=30,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0:
            return False, f"Erro compilacao: {result.stderr.strip()[:500]}", None
        return True, "Compilado como modulo", str(dll)
    except subprocess.TimeoutExpired:
        return False, "Timeout compilacao", None
    except FileNotFoundError:
        return False, "cobc nao encontrado", None
    except Exception as e:
        return False, str(e), None


def _gerar_driver(nome_convertido: str, driver_path: Path):
    """
    Gera automaticamente um driver .cob generico para chamar o modulo convertido.
    O driver passa dados via variavel de ambiente COB_PLACA (para programas de placa)
    ou apenas chama o modulo com um parametro generico.
    """
    # Ler o fonte convertido para extrair a LINKAGE SECTION
    source = CONVERTIDOS_DIR / nome_convertido
    if not source.exists():
        return

    content = source.read_text(encoding='latin-1')

    # Verificar se tem LINKAGE com LC-PARM (padrao de placas)
    has_lc_parm = "LC-PARM" in content and "LC-PLACA" in content

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
    else:
        # Driver generico - apenas chama e exibe return code
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
    driver_exe = BUILD_DIR / f"DRIVER-{nome_convertido}.exe"

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
            [_cobc(), "-x", str(driver_source), "-o", str(driver_exe)],
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

        return ResultadoCOBOL(
            programa=programa, fluxo="original", sucesso=True,
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

        return ResultadoCOBOL(
            programa=nome_convertido, fluxo="convertido", sucesso=True,
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
    cobc_exe = COBOL_BIN / "cobc.exe"
    standalone_cob = STANDALONE_DIR / "PF-GAA-L004.cob"
    standalone_exe = BUILD_DIR / "PF-GAA-L004.exe"
    convertido_src = CONVERTIDOS_DIR / "FGAA004"
    convertido_dll = BUILD_DIR / "FGAA004.dll"
    driver_exe = BUILD_DIR / "DRIVER-FGAA004.exe"

    return {
        "gnucobol_disponivel": cobc_exe.exists(),
        "compilador": str(cobc_exe),
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
