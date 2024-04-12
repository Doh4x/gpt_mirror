import os
from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

print('starting..')

@app.route('/', methods=['GET'])
@app.route('/', methods=['HEAD'])

def home():
  if "txt" in request.args:
    txt = request.args['txt']
    response = ""
    try:
      client = Client()
      
      response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": txt}],
      )
      
      response = response.choices[0].message.content
    except:
      return jsonify({"status": "ERROR", "text": "Invalid cookies"})
    return jsonify({"status": "OK", "text": response})
  else:
    return jsonify({"status": "OK", "text": ""})


app.run(debug=False,port=3000,host="0.0.0.0")