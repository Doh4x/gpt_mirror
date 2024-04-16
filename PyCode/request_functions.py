
from . import config

from g4f.client import Client
from g4f.cookies import set_cookies

from flask import jsonify


def PrintArgs(request):
    for key, value in request.lists():
        print(key + " - " + str(value), flush=True)


def try_models(txt: str):
    response = ""
    valid_provider = ""

    for provider in config["ai_models"]:
        try:
            client = Client()

            response = client.chat.completions.create(
                model=provider,
                messages=[{"role": "user", "content": txt}],
            )

            print(response.choices[0].message.content, flush=True)

            if response.choices[0].message.content in config["gpt35_error_messages"]:
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
                model=model,
                messages=[{"role": "user", "content": txt}],
            )

            if response.choices[0].message.content in config["gpt35_error_messages"]:
                response = ""
                continue

            response = response.choices[0].message.content
            valid_provider = model

            break
        finally:
            continue

    if response == "":
        return try_models()

    return jsonify({"status": "OK", "text": response or "", "provider": valid_provider, "tries_used": current_try})


def hybrid_request(txt: str, model: str):
    response = single_model_request() or ""

    if response == "" or standart_json.loads(response.get_data(as_text=True))["text"] == "":
        return try_models()
    else:
        return response
