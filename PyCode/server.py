from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from waitress import serve

import request_functions
import config

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

@app.route('/try_models', methods=['GET'])
def try_models():
    request_functions.PrintArgs(request=request)

    if "txt" in request.args:
        return request_functions.try_models(txt=request.args["txt"])
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})


@app.route('/try_single_model', methods=['GET'])
def single_model_request():
    request_functions.PrintArgs(request=request)

    if "txt" and "model" in request.args:
        return request_functions.single_model_request(txt=request.args["txt"], model=request.args["model"])
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})


@app.route('/hybrid', methods=['GET'])
def hybrid_request():
    response = ""

    if "txt" in request.args:
        return request_functions.hybrid_request(txt=request.args.get("txt"), model=request.args.get("model"))
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})

@app.route('/awake', methods=['GET'])
def awake():
    response = Response()
    response.headers.add('alive', 'OK')
    return response


@app.route('/', methods=['GET'])
def head():
    response = Response()
    response.headers.add('alive', 'OK')
    return response


serve(app, host="0.0.0.0", port=3000)
