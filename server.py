from flask import Flask, abort

app = Flask(__name__)

@app.route('/')
def index():
  return 'hi'

@app.route('/test/<command>')
def test(command):
  match comand.split('-'):
    case ['add', a, b]:
      return a + b
    case r:
      abort(400)
