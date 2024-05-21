from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps
from passwordhash import hash_password, verify_password
from auth_db import insert_user_cred, get_user_info

auth_service = Flask(__name__)
auth_service.config['SECRET_KEY'] = '5f4102db508e4065ace3df7ae799f6cf'  # Secret key for JWT



# Registration endpoint
@auth_service.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    rank = request.json.get('rank', 1)  # Default rank

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        hashed_password = hash_password(password)
        insert_user_cred(username, hashed_password, rank)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Login endpoint
@auth_service.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user_info = get_user_info(username)
    if not user_info:
        return jsonify({'error': 'Invalid username or password'}), 404

    stored_hash = user_info[1]
    rank = user_info[2]

    if verify_password(stored_hash, password):
        payload = {
            'user':username,
            'rank':rank,
            'exp': datetime.utcnow() + timedelta(minutes=30) #how long till it's unuseable

        }
        token = jwt.encode(payload, auth_service.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid password'}), 401


# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 403

        try:
            payload = jwt.decode(token.split(" ")[1], auth_service.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token!'}), 401

        return f(payload, *args, **kwargs)
    return decorated

# Test protected route # THE FOO ROUTE
@auth_service.route('/protected', methods=['GET'])
@token_required
def protected_route(payload):
    return jsonify({'message': 'This is a protected route', 'user': payload['user'], 'rank': payload['rank']})

if __name__ == '__main__':
    auth_service.run(debug=True)
