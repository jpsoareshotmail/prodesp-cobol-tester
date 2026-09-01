#!/bin/bash
# Sobe o COBOL Tester tambem na porta 443 (HTTPS) com certificado autoassinado.
# Amazon Linux. Mantem a instancia da porta 80 rodando em paralelo.
set -e
APP_DIR="$HOME/prodesp-cobol-tester"
CERT_DIR="$HOME/certs"
cd "$APP_DIR"

# 1. Gera certificado autoassinado (valido 825 dias) se ainda nao existir
mkdir -p "$CERT_DIR"
if [ ! -f "$CERT_DIR/server.crt" ]; then
    echo "Gerando certificado autoassinado..."
    openssl req -x509 -newkey rsa:2048 -nodes \
        -keyout "$CERT_DIR/server.key" -out "$CERT_DIR/server.crt" \
        -days 825 -subj "/C=BR/ST=SP/L=SaoPaulo/O=Prodesp-POC/CN=100.53.234.127"
fi

# 2. Para instancia anterior da 443
[ -f /tmp/cobol-tester-443.pid ] && sudo kill "$(cat /tmp/cobol-tester-443.pid)" 2>/dev/null || true
sleep 1

export $(grep -v '^#' .env.deploy | xargs)
USER_SITE="$(python3 -c 'import sys;print("%s/.local/lib/python%d.%d/site-packages"%(__import__("os").path.expanduser("~"),sys.version_info[0],sys.version_info[1]))')"

# 3. Sobe gunicorn na 443 com TLS (sudo pois porta privilegiada)
sudo -E env "PYTHONPATH=$USER_SITE" "SECRET_KEY=$SECRET_KEY" \
    python3 -m gunicorn web_app:app \
    --bind 0.0.0.0:443 --workers 1 --timeout 120 \
    --certfile "$CERT_DIR/server.crt" --keyfile "$CERT_DIR/server.key" \
    --daemon --pid /tmp/cobol-tester-443.pid \
    --log-file /tmp/cobol-tester-443.log

sleep 4
echo "=== STATUS porta 443 (HTTPS) ==="
curl -sk -o /dev/null -w "health: HTTP %{http_code}\n" https://localhost:443/api/health || echo "sem resposta"
echo "PID: $(sudo cat /tmp/cobol-tester-443.pid 2>/dev/null)"
tail -5 /tmp/cobol-tester-443.log
