#!/bin/bash
# Script de Build Automatizado - Sistema Legado COBOL Prodesp
# Use: bash build.sh [clean|all|test]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/PGM POC cob original"
FALTANTES="$SCRIPT_DIR/fontes_faltanters"
BUILD_DIR="$SCRIPT_DIR/build"
BIN_DIR="$BUILD_DIR/bin"
LIB_DIR="$BUILD_DIR/lib"

COBC=$(command -v cobc 2>/dev/null) || {
    echo "[ERROR] GnuCOBOL não instalado!"
    echo "Instale com:"
    echo "  Windows: https://sourceforge.net/projects/gnucobol/files/"
    echo "  Linux: apt-get install gnucobol"
    echo "  macOS: brew install gnu-cobol"
    exit 1
}

echo "========================================"
echo "Build System - COBOL Legado Prodesp"
echo "========================================"
echo ""
echo "COBC: $COBC"
echo "Versao: $($COBC --version | head -1)"
echo ""

# Funcoes
prepare() {
    echo "[*] Preparando diretorio de build..."
    mkdir -p "$BIN_DIR" "$LIB_DIR"
    echo "[OK] Diretorios criados"
}

compile_libs() {
    echo ""
    echo "[*] Compilando bibliotecas compartilhadas..."

    if [ ! -d "$FALTANTES" ]; then
        echo "[WARN] Diretorio de faltantes nao encontrado"
        return
    fi

    # Compilar copybooks principais
    for lib in SUP_SEECDT00.txt SUP_SEECDTPD.txt; do
        if [ -f "$FALTANTES/$lib" ]; then
            echo "  Compilando $lib..."
            $COBC -c "$FALTANTES/$lib" -o "$LIB_DIR/${lib%.txt}.o" 2>&1 || true
        fi
    done

    echo "[OK] Bibliotecas compiladas"
}

compile_programs() {
    echo ""
    echo "[*] Compilando programas COBOL..."

    if [ ! -d "$SRC_DIR" ]; then
        echo "[ERROR] Diretorio de fontes nao encontrado: $SRC_DIR"
        exit 1
    fi

    local count=0
    local errors=0

    cd "$SRC_DIR"

    for file in *.C74; do
        if [ -f "$file" ]; then
            count=$((count + 1))
            prog_name="${file%.C74}"
            echo "  [$count] Compilando $file..."

            if $COBC -x "$file" -I"$FALTANTES" -o "$BIN_DIR/$prog_name.exe" 2>/dev/null; then
                echo "    [OK] $prog_name.exe"
            else
                echo "    [ERRO] $prog_name.exe"
                errors=$((errors + 1))
            fi
        fi
    done

    echo ""
    echo "[*] Resumo de compilacao:"
    echo "  Total: $count"
    echo "  Sucesso: $((count - errors))"
    echo "  Erros: $errors"
}

run_tests() {
    echo ""
    echo "[*] Executando testes..."

    # Testar se Python está disponível
    if command -v python3 &>/dev/null; then
        cd "$SCRIPT_DIR"
        python3 runner.py
    elif command -v python &>/dev/null; then
        cd "$SCRIPT_DIR"
        python runner.py
    else
        echo "[WARN] Python nao encontrado - pulando testes"
    fi
}

clean() {
    echo "[*] Limpando diretorios de build..."
    rm -rf "$BUILD_DIR"
    echo "[OK] Limpeza concluida"
}

show_help() {
    cat << EOF
Uso: bash build.sh [COMANDO]

COMANDOS:
  all      Build completo (default)
  clean    Remover arquivos compilados
  test     Executar testes
  libs     Compilar apenas bibliotecas
  help     Mostrar esta mensagem

EXEMPLOS:
  bash build.sh
  bash build.sh clean
  bash build.sh test
  bash build.sh clean && bash build.sh all

ESTRUTURA GERADA:
  build/
    bin/          Executaveis (.exe)
    lib/          Bibliotecas compiladas (.o)

PROXIMOS PASSOS:
  1. ./build/bin/PF-GAA-L004.exe          Validador de placas
  2. ./build/bin/PF-GAA-B100-DB.exe       Processador BD
  3. Consulte INSTALAR_GNUCOBOL.md para mais info
EOF
}

# Main
case "${1:-all}" in
    clean)
        clean
        ;;
    libs)
        prepare
        compile_libs
        ;;
    test)
        run_tests
        ;;
    help)
        show_help
        ;;
    all|"")
        prepare
        compile_libs
        compile_programs
        echo ""
        echo "[OK] Build completo!"
        echo ""
        echo "Executaveis gerados em: $BIN_DIR"
        ls -lh "$BIN_DIR" 2>/dev/null | tail -10 || true
        ;;
    *)
        echo "[ERROR] Comando desconhecido: $1"
        show_help
        exit 1
        ;;
esac

echo ""
echo "========================================"
