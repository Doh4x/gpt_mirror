set -eux
. /tmp/venv/bin/activate
flask --app PyCode/server run --port $PORT
