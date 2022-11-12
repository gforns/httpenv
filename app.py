from flask import Flask, request
import os
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "\nHTTPenv image:\n\n /anything: to print requests info\n /env: to print envars\n /all: to print all\n\n"


@app.route("/env", methods = ['GET','POST','PUT','DELETE','HEAD'])
def env():
    env_var = dict(os.environ)
    return json.dumps(env_var, indent=2)

@app.route("/anything", methods = ['GET','POST','PUT','DELETE','HEAD'])
def anything():
    a = {}
    a['headers'] = dict(request.headers)
    a['args'] = dict(request.args)
    a['form'] = dict(request.form)
    a['json'] = request.json
    a['method'] = request.method
    a['origin'] = request.origin
    a['url'] = request.url
    return json.dumps(a, indent=2)

@app.route("/all", methods = ['GET','POST','PUT','DELETE','HEAD'])
def all():
    a = {}
    a['headers'] = dict(request.headers)
    a['args'] = dict(request.args)
    a['form'] = dict(request.form)
    a['json'] = request.json
    a['method'] = request.method
    a['origin'] = request.origin
    a['url'] = request.url
    env_var = dict(os.environ)
    return json.dumps( {"request": a, "env": env_var },  indent=2)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False,host='0.0.0.0',port=port)