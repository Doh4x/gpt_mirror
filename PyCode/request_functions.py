
from . import config

from g4f.client import Client
from g4f.cookies import set_cookies

from flask import jsonify
import json as standart_json

def PrintArgs(request):
    for key, value in request.lists():
        print(key + " - " + str(value), flush=True)


def try_models(txt: str):
    response = ""
    valid_provider = ""

    for provider in config.ai_models:
        try:
            client = Client()

            response = client.chat.completions.create(
                model=provider,
                messages=[{"role": "user", "content": txt}],
            )

            if response.choices[0].message.content in config.gpt35_error_messages:
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


def single_model_request(txt: str, model: str):
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
            
            if response.choices[0].message.content in config.gpt35_error_messages:
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


def hybrid_request(txt: str, model: str):
    response = single_model_request(txt=txt, model=model)

    if response == "" or standart_json.loads(response.get_data(as_text=True))["text"] == "":
        return try_models(txt=txt)
    else:
        return response
