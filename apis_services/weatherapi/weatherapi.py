import os
from flask import Flask, jsonify
from getLastData import getData, getOutsideTemp
from functools import wraps
from flask import request, abort

app = Flask(__name__)

keys =[]
apifile = os.path.expanduser('~/.ssh/weatherapi.keys')
if os.path.isfile(apifile):
    with open(apifile, 'r') as apikey:
        lis=apikey.readlines()
    for k in lis:
        k, _ = k.split(',')
        keys.append(k)


def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') in keys:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@app.route('/values')
@require_appkey
def get_values():
    fname = os.getenv('DATAFILE', default='/home/pi/weather/weatherdata.json')
    values=[getData(fname)]
    return jsonify(values)


@app.route('/tempout')
@require_appkey
def get_tempout():
    fname = os.getenv('DATAFILE', default='/home/pi/weather/weatherdata.json')
    values=[getOutsideTemp(fname)]
    return jsonify(values)


@app.route('/')
def show_info():
    return 'usage: url?/values'
