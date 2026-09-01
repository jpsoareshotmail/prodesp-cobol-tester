#!/bin/bash
# Reinicia o COBOL Tester na porta 80 (publica) com gunicorn + sudo.
# Roda NA EC2.
set -e
APP_DIR="$HOME/prodesp-cobol-tester"
cd "$APP_DIR"

# para instancias anteriores (porta 5000 e 80)
[ -f /tmp/cobol-tester.pid ] && kill "$(cat /tmp/cobol-tester.pid)" 2>/dev/null || true
[ -f /tmp/cobol-tester-80.pid ] && sudo kill "$(cat /tmp/cobol-tester-80.pid)" 2>/dev/null || true
sleep 1

# carrega SECRET_KEY
export $(grep -v '^#' .env.deploy | xargs)
export PATH="$HOME/.local/bin:$PATH"

# sobe na porta 80 (privilegiada -> sudo -E preserva env)
sudo -E "$HOME/.local/bin/gunicorn" web_app:app \
    --bind 0.0.0.0:80 --workers 2 --timeout 120 \
    --daemon --pid /tmp/cobol-tester-80.pid \
    --log-file /tmp/cobol-tester-80.log

sleep 3
echo "=== Status porta 80 ==="
curl -s -o /dev/null -w "health: HTTP %{http_code}\n" http://localhost:80/api/health || echo "sem resposta"
echo "PID: $(cat /tmp/cobol-tester-80.pid 2>/dev/null)"
echo "Log: tail -f /tmp/cobol-tester-80.log"
