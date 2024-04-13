import os

from flask import Flask, request, jsonify
from g4f.client import Client
from g4f.cookies import set_cookies

app = Flask(__name__)

ai_providers = ['gemini',  'gemini-pro']

set_cookies(".google.com", {
   "__Secure-1PSID": os.environ['gemini_cookie'],
   "gemini_cookie[__Secure-1PSIDCC]": os.environ['gemini_cookie'],
   "__Secure-1PSID": os.environ['gemini_cookie'],
   "__Secure-1PSID": os.environ['gemini_cookie'],
})

client = Client()

@app.route('/', methods=['GET'])

def home():
  if "txt" in request.args:
    txt = request.args['txt']
    response = ""
    valid_provider = ""
    
    for provider in ai_providers:
      try:
        print(provider, os.environ['gemini_cookie'], flush=True)
        
        client = Client()
      
        response = client.chat.completions.create(
            model=provider,
            messages=[{"role": "user", "content": txt}],
        )

        if response.choices[0].message.content == "\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883":
          continue
        
        response = response.choices[0].message.content
        valid_provider = provider
        
        break
      except:
        continue

    if response == "":
       return jsonify({"status": "NOT OK", "text": "Invalid cookies", "provider": valid_provider})
      
    return jsonify({"status": "OK", "text": response, "provider": valid_provider})
  else:
    return jsonify({"status": "OK", "text": ""})

@app.route('/', methods=['HEAD'])

def head():
    response = Response()
    response.headers.add('alive', 'OKAY')
    return response
  
app.run(debug=False,port=3000,host="0.0.0.0")