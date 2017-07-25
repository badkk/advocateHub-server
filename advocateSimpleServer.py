from flask import Flask, json, session
from flask import request
from flask import make_response
from flask_cors import CORS
from bson import json_util
import time
import os

app = Flask(__name__)
CORS(app)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "templates")
app.secret_key = 'SUPERSECRETEKEYOFMSADVOCATEHUB'

#
# Functions
#

def jd(obj):
    return json_util.dumps(obj)


#
# Response
#

def response(data={}, code=200):
    resp = {
        "timestamp": int(round(time.time() * 1000)),
        "status": code,
        "data": data
    }
    response = make_response(jd(resp))
    response.headers['Status Code'] = resp['status']
    response.headers['Content-Type'] = "application/json"
    return response


#
# Error handing
#

@app.errorhandler(404)
def page_not_found(error):
    return response({}, 404)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user')
def get_user():
    user = open(json_url + '/user.json')
    return response(json.load(user))


@app.route('/advocators')
def get_advocators():
    advocators = open(json_url + '/advocates.json')
    return response(json.load(advocators))


@app.route('/azure/infos')
def get_azureInfos():
    info = open(json_url + '/azureInfos.json')
    return response(json.load(info))


@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        userInfo = request.get_json()
        session['id'] = userInfo['id']
        return response(True)
    else:
        userId = request.args.get('userId')
        #add the mongo query in here
        if userId == '1284688014':
            return response(True)
        return response(False)
        #return response(('id' in session))


if __name__ == '__main__':
    app.run(host='localhost', port=13888, debug=True)
