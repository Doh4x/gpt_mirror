set -eux
. /tmp/venv/bin/activate
flask --app server run --port $PORT
