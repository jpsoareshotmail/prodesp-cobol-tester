#!/bin/bash
# =============================================================================
# Deploy do COBOL Tester na EC2 (Amazon Linux 2023)
# Roda NA EC2. Instala deps, GnuCOBOL do sistema, clona o repo e sobe via gunicorn.
#
# Uso (do Windows, na pasta do projeto):
#   ssh -i vmchaves/poc-prodesp-kp.pem ec2-user@<IP> "bash -s" < deploy/deploy-ec2.sh
#
# IMPORTANTE: os fontes COBOL (fontes_convertidos/, PGM POC cob original/) e o
# cobol_build/copy/ estao no .gitignore e NAO vem pelo git clone. Envie-os
# separadamente via scp (ver deploy/enviar-fontes.sh) ou o app roda so em
# modo simulacao Python (sem compilar COBOL real).
# =============================================================================
set -e
echo "=== DEPLOY COBOL TESTER (EC2 Linux) ==="

REPO_URL="https://github.com/jpsoareshotmail/prodesp-cobol-tester.git"
APP_DIR="$HOME/prodesp-cobol-tester"
PORT="${PORT:-5000}"

# 1. Dependencias do sistema
echo "[1/6] Instalando dependencias do sistema..."
sudo dnf install -y python3 python3-pip gcc git

# 2. GnuCOBOL (compilador COBOL) - do repositorio; se falhar, compila do source
echo "[2/6] Instalando GnuCOBOL..."
if ! command -v cobc >/dev/null 2>&1; then
    sudo dnf install -y gnucobol || {
        echo "  Pacote nao encontrado; compilando do source..."
        sudo dnf install -y gmp-devel libdb-devel ncurses-devel wget tar make
        cd /tmp
        wget -q "https://sourceforge.net/projects/gnucobol/files/gnucobol/3.2/gnucobol-3.2.tar.gz/download" -O gnucobol-3.2.tar.gz
        tar xzf gnucobol-3.2.tar.gz && cd gnucobol-3.2
        ./configure --prefix=/usr/local && make -j"$(nproc)" && sudo make install && sudo ldconfig
        cd "$HOME"
    }
fi
cobc --version >/dev/null 2>&1 && echo "  GnuCOBOL OK: $(cobc --version | head -1)" || echo "  AVISO: cobc indisponivel (app rodara em modo simulacao)"

# 3. Clonar/atualizar o projeto
echo "[3/6] Obtendo o projeto..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR" && git pull
else
    git clone "$REPO_URL" "$APP_DIR" && cd "$APP_DIR"
fi

# 4. Dependencias Python (inclui gunicorn)
echo "[4/6] Instalando dependencias Python..."
pip3 install --user -r requirements.txt
export PATH="$HOME/.local/bin:$PATH"

# 5. Variaveis de ambiente (SECRET_KEY fixo p/ sessao nao cair a cada restart)
echo "[5/6] Configurando ambiente..."
ENV_FILE="$APP_DIR/.env.deploy"
if [ ! -f "$ENV_FILE" ]; then
    echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > "$ENV_FILE"
    echo "  SECRET_KEY gerado em $ENV_FILE"
fi
export $(grep -v '^#' "$ENV_FILE" | xargs)

# 6. Subir o servidor com gunicorn (producao), matando instancia anterior
echo "[6/6] Iniciando servidor (gunicorn) na porta $PORT..."
[ -f /tmp/cobol-tester.pid ] && kill "$(cat /tmp/cobol-tester.pid)" 2>/dev/null || true
cd "$APP_DIR"
nohup "$HOME/.local/bin/gunicorn" web_app:app \
    --bind "0.0.0.0:$PORT" --workers 1 --timeout 120 \
    > /tmp/cobol-tester.log 2>&1 &
echo $! > /tmp/cobol-tester.pid

sleep 3
echo ""
echo "=== DEPLOY COMPLETO ==="
echo "URL:   http://<IP-DA-EC2>:$PORT"
echo "Login: admin / prodesp_2026  (troque a senha no primeiro acesso)"
echo "Log:   tail -f /tmp/cobol-tester.log"
echo "PID:   $(cat /tmp/cobol-tester.pid)"
echo "Parar: kill \$(cat /tmp/cobol-tester.pid)"
