#!/bin/bash
# =============================================================================
# Deploy do COBOL Tester em EC2 Ubuntu (24.04/26.04)
# Roda NA EC2. Instala deps + GnuCOBOL (apt), clona o repo e sobe via gunicorn.
#
# Uso (do Windows, na pasta do projeto):
#   Get-Content deploy\deploy-ubuntu.sh -Raw | ssh -i vmchaves\prodesp_teste.pem ubuntu@<IP> "bash -s"
#
# Obs: instancia com ~900MB RAM -> usa 1 worker no gunicorn.
# Fontes COBOL (fontes_convertidos/, cobol_build/copy/) vao por scp separado.
# =============================================================================
set -e
echo "=== DEPLOY COBOL TESTER (Ubuntu) ==="

REPO_URL="https://github.com/jpsoareshotmail/prodesp-cobol-tester.git"
APP_DIR="$HOME/prodesp-cobol-tester"
PORT="${PORT:-5000}"

echo "[1/6] Atualizando indice apt e instalando dependencias..."
sudo apt-get update -y -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    python3 python3-pip python3-venv git gnucobol build-essential

echo "[2/6] Verificando GnuCOBOL..."
cobc --version >/dev/null 2>&1 && echo "  GnuCOBOL OK: $(cobc --version | head -1)" || echo "  AVISO: cobc indisponivel (modo simulacao)"

echo "[3/6] Obtendo o projeto..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR" && git pull
else
    git clone "$REPO_URL" "$APP_DIR" && cd "$APP_DIR"
fi

echo "[4/6] Ambiente virtual + dependencias Python..."
cd "$APP_DIR"
python3 -m venv .venv
. .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo "[5/6] Configurando ambiente (SECRET_KEY)..."
ENV_FILE="$APP_DIR/.env.deploy"
if [ ! -f "$ENV_FILE" ]; then
    echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > "$ENV_FILE"
fi
export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "[6/6] Iniciando gunicorn (1 worker) na porta $PORT..."
[ -f /tmp/cobol-tester.pid ] && kill "$(cat /tmp/cobol-tester.pid)" 2>/dev/null || true
sleep 1
nohup .venv/bin/gunicorn web_app:app \
    --bind "0.0.0.0:$PORT" --workers 1 --timeout 120 \
    > /tmp/cobol-tester.log 2>&1 &
echo $! > /tmp/cobol-tester.pid

sleep 4
echo ""
echo "=== STATUS ==="
curl -s -o /dev/null -w "health local: HTTP %{http_code}\n" "http://localhost:$PORT/api/health" || echo "sem resposta"
echo "PID: $(cat /tmp/cobol-tester.pid)"
echo "Log: tail -f /tmp/cobol-tester.log"
echo ""
echo "URL: http://54.81.98.44:$PORT  (liberar porta $PORT no Security Group)"
echo "Login: admin / prodesp_2026"
