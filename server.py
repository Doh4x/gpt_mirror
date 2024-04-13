import os
import sys

from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

client = Client()

print('This is error output', file=sys.stderr)
print('This is standard output', file=sys.stdout)

@app.route('/', methods=['GET'])

def home():
  print("GOT REQUEST")
  
  if "txt" in request.args:
    txt = request.args['txt']
    response = ""
  
    try:   
      response = client.chat.completions.create(
          model='pi',
          messages=[{"role": "user", "content": txt}],
      )
      
      response = response
    finally:
      return jsonify({"status": "OK", "text": response})
  else:
    return jsonify({"status": "OK", "text": ""})

@app.route('/', methods=['HEAD'])

def head():
    response = Response()
    response.headers.add('alive', 'OKAY')
    return response
  
app.run(debug=False,port=3000,host="0.0.0.0")