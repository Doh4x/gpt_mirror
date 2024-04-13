import os

from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

client = Client()

@app.route('/', methods=['GET'])

def home():
  if "txt" in request.args:
    txt = request.args['txt']
    response = ""
  
    print(txt, flush=True)
    
    #try:
    response = client.chat.completions.create(
          model='pi',
          messages=[{"role": "user", "content": txt}],
    )
      
    print("request.args", flush=True)
        
    response = response.choices[0].message.content
   # finally:
    return jsonify({"status": "OK", "text": response})
  else:
    return jsonify({"status": "OK", "text": ""})

@app.route('/', methods=['HEAD'])

def head():
    response = Response()
    response.headers.add('alive', 'OKAY')
    return response
  
app.run(debug=False,port=3000,host="0.0.0.0")