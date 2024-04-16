import os
import json as standart_json

from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response, json
from waitress import serve

import g4f
from g4f.client import Client
from g4f.cookies import set_cookies

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

ai_models = ['gpt-3.5-long', 'gpt-3.5-turbo', 'llama2-70b', 'dolphin-mixtral-8x7b']
gpt35_error_messages = [
  '\u6d41\u91cf\u5f02\u5e38,\u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883', 
  '\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883'
]

def PrintArgs():
   for key, value in request.args.lists():
     print(key + " - " + str(value), flush=True)
    
@app.route('/try_models', methods=['GET'])

def try_models():
  PrintArgs()
  
  if "txt" in request.args:
    txt = request.args['txt']
    response = ""
    valid_provider = ""
    
    for provider in ai_models:
      try:
        client = Client()
        
        response = client.chat.completions.create(
            model=provider,
            messages=[{"role": "user", "content": txt}],
        )
        
        print(response.choices[0].message.content, flush=True)
        
        if response.choices[0].message.content in gpt35_error_messages:
          continue
            
        response = response.choices[0].message.content
        valid_provider = provider
        
        break
      except:
        continue

    if response == "":
       return jsonify({"status": "NOT OK", "text": "Invalid cookies", "provider": "", "tries_used": "1"})
    
    return jsonify({"status": "OK", "text": response or "", "provider": valid_provider})
  else:
    return jsonify({"status": "OK", "text": "", "provider": "", "tries_used": "1"})

@app.route('/try_single_model', methods=['GET'])

def single_model_request():
  PrintArgs()
  
  if "txt" and "model" in request.args:
    txt = request.args['txt']
    model = request.args['model']
    
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
        
        if response.choices[0].message.content in gpt35_error_messages:
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
  else:
    return jsonify({"status": "OK", "text": "", "provider": "", "tries_used": "1"})

@app.route('/hybrid', methods=['GET'])

def hybrid_request():
  print(request.args['txt'], flush=True)
  
  response = ""
  
  if "txt" in request.args:
    response = single_model_request()
  
  if response == "" or standart_json.loads(response.get_data(as_text=True))["text"] == "":
    return try_models()
  else:
    return response

@app.route('/get_stoty', methods=['GET'])

def game_story_config():
 print(request.args['txt'], flush=True)

 response = ""
 
 hybrid_request()

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