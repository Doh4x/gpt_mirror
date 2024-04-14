import os

from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from g4f.client import Client
from g4f.cookies import set_cookies

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
client = Client()

ai_providers = ['gpt-3.5-long', 'llama2-70b', 'gpt-4', 'dolphin-mixtral-8x7b']
gpt35_error_messages = [
  '\u6d41\u91cf\u5f02\u5e38,\u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883', 
  '\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883'
                       ]
  
@app.route('/', methods=['GET'])

def home():
  if "txt" in request.args:
    txt = request.args['txt']
    response = ""
    valid_provider = ""
      
    for provider in ai_providers:
      print(provider, flush=True)
      
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
       return jsonify({"status": "NOT OK", "text": "Invalid cookies", "provider": ""})
    
    return jsonify({"status": "OK", "text": response or "", "provider": valid_provider})
  else:
    return jsonify({"status": "OK", "text": ""})

@app.route('/', methods=['HEAD'])

def head():
    response = Response()
    response.headers.add('alive', 'OK')
    return response

app.run(debug=False,port=3000,host="0.0.0.0")
#serve(app, host="0.0.0.0", port=3000)