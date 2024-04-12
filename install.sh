set -eux
python3 -m venv /tmp/venv
. /tmp/venv/bin/activate
python3 -m pip --cache-dir /tmp/pip-cache install -r requirements-stealth.txt
