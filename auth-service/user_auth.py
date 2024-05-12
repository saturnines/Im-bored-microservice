from flask import Flask, request, jsonify, make_response, render_template, session

import jwt
from datetime import datetime, timedelta
from functools import wraps





auth_service = Flask(__name__, template_folder='C:/Users/Kevin/Desktop/bored_microservice/templates')
auth_service.config['SECRET_KEY'] = '5f4102db508e4065ace3df7ae799f6cf'  # I suppose this is the  secret key for jwt vertifying


# Login and Reg Part:








# JWT Part.
def token_Required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = jwt.decode(token, auth_service.config['SECRET_KEY'])
        except:
            return jsonify({'Alert!':'Invalid Token!'})
    return decorated()

@auth_service.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!'

#public
@auth_service.route('/public')
def public():
    return 'for public'

#authg
@auth_service.route('authenticate')
@token_Required
def auth():
    return 'JWT is verified.'


@auth_service.route('/login', methods=['POST'])
def login():
    """Logins and checks if the jwt is right, and also adds an expirary to the jwt token"""
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True #???
        token = jwt.encode({
            'user':request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        },
            auth_service.config['SECRET_KEY'])
        return jsonify({'token':token.decode('uft-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate':'Basic realm: "Authentication Failed!'})



