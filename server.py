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

ai_providers = ['gpt-3.5-turbo', 'llama2-7b', 'gpt-4']

set_cookies(".google.com", {
   "__Secure-1PSID": os.environ.get('__Secure-1PSID'),
   "__Secure-1PSIDCC": os.environ.get('__Secure-1PSIDCC'),
   "__Secure-1PSIDTS": os.environ.get('__Secure-1PSIDTS'),
   "SSID": os.environ.get('SSID'),
})

  
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
        
        if response.choices[0].message.content == "\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883":
          continue
        
        print(provider, flush=True)
        print(response.choices[0].message.model, flush=True)
            
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