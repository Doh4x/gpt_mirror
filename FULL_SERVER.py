from flask import Flask, request, jsonify
import json as standart_json

import sys
import pkg_resources

from g4f.client import Client

ai_models = ['gpt-3.5-long', 'gpt-3.5-turbo', 'llama2-70b', 'dolphin-mixtral-8x7b']

gpt35_error_messages = [
    '\u6d41\u91cf\u5f02\u5e38,\u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883',
    '\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883'
]

def try_models_function(txt: str):
    response = ""
    valid_provider = ""

    for provider in ai_models:
        try:
            client = Client()

            response = client.chat.completions.create(
                model=provider,
                messages=[{"role": "user", "content": txt}],
            )

            if response.choices[0].message.content in gpt35_error_messages:
                response = ""
                
                continue

            response = response.choices[0].message.content
            valid_provider = provider

            break
        except:
            continue

    if response == "":
        return jsonify({"status": "NOT OK", "text": "Invalid cookies", "provider": "", "tries_used": "1"})

    return jsonify({"status": "OK", "text": response or "", "provider": valid_provider})


def single_model_request_function(txt: str, model: str):
    response = ""
    valid_provider = ""
    maximum_tries = 10
    current_try = 0

    while response == "" and current_try < maximum_tries:
        current_try += 1

        try:
            client = Client()

            response = client.chat.completions.create(
                model= not model == "" and model or 'llama2-70b',
                messages=[{"role": "user", "content": txt}],
            )
            
            if response.choices[0].message.content in gpt35_error_messages:
                response = ""
                
                continue

            response = response.choices[0].message.content
            valid_provider = model

            break
        finally:
            continue

    if response == "":
        return jsonify({"status": "NOT OK", "text": "", "provider": not model == "" and model or 'ERROR', "tries_used": current_try})
    
    return jsonify({"status": "OK", "text": response, "provider": not model == "" and model or 'llama2-70b', "tries_used": current_try})


def hybrid_request_function(txt: str, model: str):
    response = single_model_request_function(txt=txt, model=model)

    if response == "" or standart_json.loads(response.get_data(as_text=True))["text"] == "":
        return try_models_function(txt=txt)
    else:
        return response

application = Flask(__name__)

@application.route('/try_models', methods=['GET'])
def try_models():
    if "txt" in request.args:
        ai_response = ""

        try:
            ai_response = try_models_function(txt=request.args["txt"])
        except Exception as e:
            return jsonify({"status": "NOT OK", "error": "<p>Error: %s</p>" % str(e)})

        return ai_response
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})


@application.route('/try_single_model', methods=['GET'])
def single_model_request():
    if "txt" and "model" in request.args:
        return single_model_request_function(txt=request.args["txt"], model=request.args["model"])
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})


@application.route('/hybrid', methods=['GET'])
def hybrid_request():
    response = ""

    if "txt" in request.args:
        return hybrid_request_function(txt=request.args.get("txt"), model=request.args.get("model") or "")
    else:
        return jsonify({"status": "NOT OK", "text": "", "provider": "", "tries_used": "1"})

@application.route('/awake', methods=['GET'])
def awake():
    return jsonify({"status": "OK", "running": "true"})

@application.route('/test', methods=['GET'])
def test():
    try:
        import g4f
    except Exception as e:
        return jsonify({"status": "OK", "running": "true", "error" : "<p>Error: %s</p>" % str(e)})
        
    installed_packages = [i.key for i in pkg_resources.working_set]
    return jsonify({"status": "OK", "running": "true", "python" : sys.version, "packages" : installed_packages})

@application.route('/', methods=['GET'])
def head():
    installed_packages = [i.key for i in pkg_resources.working_set]
    return jsonify({"status": "OK", "running": "true", "python" : sys.version, "packages" : installed_packages})

if __name__ == "__main__":
    application.run(host='0.0.0.0',debug=True)