from flask import Flask, request, jsonify, make_response, render_template, session

import jwt
from datetime import datetime, timedelta
from functools import wraps
from passwordhash import hash_password, verify_password
from auth_db import insert_user_cred,delete_user_cred, get_user_info
from flask import Response



auth_service = Flask(__name__, template_folder='C:/Users/Kevin/Desktop/bored_microservice/templates')
auth_service.config['SECRET_KEY'] = '5f4102db508e4065ace3df7ae799f6cf'  # I suppose this is the  secret key for jwt vertifying


# Login and Reg Part:
@auth_service.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or password:
        return jsonify({'error': 'Missing username or password'}), 400
    try:
        hashed_password = hash_password(password)
        insert_user_cred(username, hashed_password)
        return jsonify({'message': 'User registered successfully'}), 201
     except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_service.route()
def log_in():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or password:
        return jsonify({'error': 'Missing username or password'}), 400





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



