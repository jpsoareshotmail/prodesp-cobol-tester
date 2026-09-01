#!/bin/bash
# Deploy so da aplicacao (assume deps + GnuCOBOL ja instalados).
# Clona/atualiza, instala Python deps com --user e sobe o gunicorn (1 worker).
set -e
echo "=== DEPLOY APP (deps ja instaladas) ==="

REPO_URL="https://github.com/jpsoareshotmail/prodesp-cobol-tester.git"
APP_DIR="$HOME/prodesp-cobol-tester"
PORT="${PORT:-5000}"

echo "[1/4] Obtendo o projeto..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR" && git pull
else
    git clone "$REPO_URL" "$APP_DIR" && cd "$APP_DIR"
fi

echo "[2/4] Dependencias Python (pip --user)..."
pip3 install --user --quiet -r requirements.txt
export PATH="$HOME/.local/bin:$PATH"

echo "[3/4] SECRET_KEY..."
ENV_FILE="$APP_DIR/.env.deploy"
[ -f "$ENV_FILE" ] || echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > "$ENV_FILE"
export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "[4/4] Subindo gunicorn (1 worker) na porta $PORT..."
[ -f /tmp/cobol-tester.pid ] && kill "$(cat /tmp/cobol-tester.pid)" 2>/dev/null || true
sleep 1
cd "$APP_DIR"
nohup "$HOME/.local/bin/gunicorn" web_app:app \
    --bind "0.0.0.0:$PORT" --workers 1 --timeout 120 \
    > /tmp/cobol-tester.log 2>&1 &
echo $! > /tmp/cobol-tester.pid

sleep 4
echo "=== STATUS ==="
curl -s -o /dev/null -w "health: HTTP %{http_code}\n" "http://localhost:$PORT/api/health" || echo "sem resposta"
echo "PID: $(cat /tmp/cobol-tester.pid)"
tail -5 /tmp/cobol-tester.log
