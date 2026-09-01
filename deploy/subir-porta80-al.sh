#!/bin/bash
# Reinicia o COBOL Tester na porta 80 (Amazon Linux, gunicorn --user + sudo).
set -e
APP_DIR="$HOME/prodesp-cobol-tester"
cd "$APP_DIR"

# para instancias anteriores (5000 e 80)
[ -f /tmp/cobol-tester.pid ] && kill "$(cat /tmp/cobol-tester.pid)" 2>/dev/null || true
[ -f /tmp/cobol-tester-80.pid ] && sudo kill "$(cat /tmp/cobol-tester-80.pid)" 2>/dev/null || true
sleep 1

export $(grep -v '^#' .env.deploy | xargs)

# gunicorn foi instalado com pip --user (site-packages do ec2-user).
# Ao rodar com sudo (root), precisamos apontar o PYTHONPATH para esse local
# e chamar via 'python3 -m gunicorn'.
USER_SITE="$(python3 -c 'import site,os;print(os.path.expanduser("~/.local/lib/python%d.%d/site-packages"%(__import__("sys").version_info[:2])))')"
echo "user site-packages: $USER_SITE"

sudo -E env "PYTHONPATH=$USER_SITE" "SECRET_KEY=$SECRET_KEY" \
    python3 -m gunicorn web_app:app \
    --bind 0.0.0.0:80 --workers 1 --timeout 120 \
    --daemon --pid /tmp/cobol-tester-80.pid \
    --log-file /tmp/cobol-tester-80.log

sleep 4
echo "=== STATUS porta 80 ==="
curl -s -o /dev/null -w "health: HTTP %{http_code}\n" http://localhost:80/api/health || echo "sem resposta"
echo "PID: $(sudo cat /tmp/cobol-tester-80.pid 2>/dev/null)"
tail -5 /tmp/cobol-tester-80.log
