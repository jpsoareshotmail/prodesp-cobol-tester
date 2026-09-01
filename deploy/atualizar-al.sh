#!/bin/bash
# Atualiza o codigo (git pull) e reinicia o app nas portas 80 e 443 (Amazon Linux).
set -e
APP_DIR="$HOME/prodesp-cobol-tester"
CERT_DIR="$HOME/certs"
cd "$APP_DIR"

echo "[1/3] Atualizando codigo..."
git pull

export $(grep -v '^#' .env.deploy | xargs)
USER_SITE="$(python3 -c 'import sys;print("%s/.local/lib/python%d.%d/site-packages"%(__import__("os").path.expanduser("~"),sys.version_info[0],sys.version_info[1]))')"

echo "[2/3] Reiniciando porta 80..."
[ -f /tmp/cobol-tester-80.pid ] && sudo kill "$(cat /tmp/cobol-tester-80.pid)" 2>/dev/null || true
sleep 1
sudo -E env "PYTHONPATH=$USER_SITE" "SECRET_KEY=$SECRET_KEY" \
    python3 -m gunicorn web_app:app --bind 0.0.0.0:80 --workers 1 --timeout 120 \
    --daemon --pid /tmp/cobol-tester-80.pid --log-file /tmp/cobol-tester-80.log

echo "[3/3] Reiniciando porta 443..."
[ -f /tmp/cobol-tester-443.pid ] && sudo kill "$(cat /tmp/cobol-tester-443.pid)" 2>/dev/null || true
sleep 1
sudo -E env "PYTHONPATH=$USER_SITE" "SECRET_KEY=$SECRET_KEY" \
    python3 -m gunicorn web_app:app --bind 0.0.0.0:443 --workers 1 --timeout 120 \
    --certfile "$CERT_DIR/server.crt" --keyfile "$CERT_DIR/server.key" \
    --daemon --pid /tmp/cobol-tester-443.pid --log-file /tmp/cobol-tester-443.log

sleep 4
echo "=== STATUS ==="
curl -s  -o /dev/null -w "porta80:  HTTP %{http_code}\n" http://localhost/api/health || echo "80 sem resposta"
curl -sk -o /dev/null -w "porta443: HTTP %{http_code}\n" https://localhost/api/health || echo "443 sem resposta"
