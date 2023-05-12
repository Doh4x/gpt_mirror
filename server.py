import math

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  return 'hi'

@app.route('/test/<command>')
def test(command):
  match command.split('-'):
    case ['add', a, b]:
      return str(int(a) + int(b))
    case ['multiply', a, b]:
      return str(int(a) * int(b))
    case ['ln', x]:
      return str(math.log(float(x)))
    case _:
      flask.abort(400)
