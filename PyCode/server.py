from os.path import join, dirname
from flask import Flask, request, jsonify
from pathlib import Path

import os
import sys
import urllib
import pkg_resources
        
sys.path.append(os.getcwd())
from . import request_functions
from . import config

application = Flask(__name__)

@application.route('/try_models', methods=['GET'])
def try_models():
    request_functions.PrintArgs(request=request)

    if "txt" in request.args:
        return request_functions.try_models(txt=config.ai_introduction + request.args["txt"])
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})


@application.route('/try_single_model', methods=['GET'])
def single_model_request():
    request_functions.PrintArgs(request=request)

    if "txt" and "model" in request.args:
        return request_functions.single_model_request(txt=config.ai_introduction + request.args["txt"], model=request.args["model"])
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})

@application.route('/hybrid', methods=['GET'])
def hybrid_request():
    response = ""

    if "txt" in request.args:
        return request_functions.hybrid_request(txt=config.ai_introduction + request.args.get("txt"), model=request.args.get("model") or "")
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})


@application.route('/awake', methods=['GET'])
def awake():
    return jsonify({"status": "OK", "running": "true"})


@application.route('/asincio_test', methods=['GET'])
def asincio_test():
    return jsonify({"result": "OK", "running": "true", "working_models": request_functions.start_test()})

@application.route('/get_game_stats', methods=['GET'])
def get_game_stats():
    if "universe_id" in request.args:
        response = ""

        try:
            response = urllib.request.urlopen("https://games.roblox.com/v1/games?universeIds=" + request.args["universe_id"]).read()
        except Exception as e:
            return jsonify({"status": "NOT OK", "error": "<p>Error: %s</p>" % str(e)})

        return jsonify({"status": "OK", "text": str(response)})
    else:
        return jsonify({"status": "NOT OK", "text": ""})

@application.route('/test', methods=['GET'])
def test():
    try:
        return jsonify({"result": "OK", "running": "true", "working_models": request_functions.start_test()})
    except Exception as e:
        return jsonify({"status": "NOT OK", "running": "true", "error" : "<p>Error: %s</p>" % str(e)})

@application.route('/', methods=['GET', 'HEAD'])
def head():
    installed_packages = [i.key for i in pkg_resources.working_set]
    return jsonify({"status": "OK", "running": "true", "packages": installed_packages, "current_path": str(Path(__file__))})

if __name__ == "__main__":
    application.run(host='0.0.0.0')
