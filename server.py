import math

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  return flask.send_file('index.html')

@app.route('/test/<command>')
def test(command):
  # check this out, match!
  # https://peps.python.org/pep-0636/
  match command.split('-'):
    case ['add', a, b]:
      return str(int(a) + int(b))
    case ['multiply', a, b]:
      return str(int(a) * int(b))
    case ['ln', x]:
      return str(math.log(float(x)))
    case _:
      flask.abort(400)
