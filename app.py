from flask import Flask, request
import os
import json
import time

app = Flask(__name__)

@app.route("/")
def hello():
    service_name = os.environ.get("MYSERVICE", "No MYSERVICE envar set")
    response_txt = "HTTPenv running on '" + service_name + "' (browse '/help' to show more options)\n"
    return response_txt


@app.route("/help")
def help():
    return "HTTPenv image:\n\n \
    '/': if a MYSERVICE envar is set it will show it\n \
    '/anything': to print requests info\n \
    '/env': to print envars\n \
    '/all': to print all\n \
    '/delay/<n>': to delay 'all' response <n> seconds\n\n"

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


@app.route("/delay/<seconds>", methods = ['GET','POST','PUT','DELETE','HEAD'])
def delay(seconds):
    try: 
        time.sleep(int(seconds))
    except:
        time.sleep(5)
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
    ssl = os.environ.get("SSL")

    if ssl and ssl != "False":
        app.run(debug=False,host='0.0.0.0',port=port, ssl_context='adhoc')
    else:    
        app.run(debug=False,host='0.0.0.0',port=port)