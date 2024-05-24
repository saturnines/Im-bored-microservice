import sys
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from suggestion_service import crud_services
import jwt
from functools import wraps
from auth_service import user_auth
import bcrypt

sys.path.append(r"C:\Users\Kevin\Desktop\bored_microservice")  # Change this for AWS.

gateway_service = Flask(__name__)
gateway_service.config['SECRET_KEY'] = '5f4102db508e4065ace3df7ae799f6cf'

def token_required(allowed_roles):
    """Check for JWT token and allowed roles."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'Alert!': 'Token is missing!'}), 403

            try:
                payload = jwt.decode(token.split(" ")[1], gateway_service.config['SECRET_KEY'], algorithms=['HS256'])
                if payload['rank'] not in allowed_roles:
                    return jsonify({'error': 'Access denied!'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'Alert!': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'Alert!': 'Invalid Token!'}), 401

            return f(payload, *args, **kwargs)
        return wrapper
    return decorator

# Suggestion Endpoints
@gateway_service.route('/delete_entry', methods=['DELETE'])
@token_required(allowed_roles=[2])
def delete_suggestion():
    category = request.json.get('category')
    title = request.json.get('title')
    description = request.json.get('description')

    if not category or not title or not description:
        return jsonify({'error': 'Missing category, title, or description!'}), 406

    try:
        crud_services.delete_entry(category, title, description)
        return jsonify({'message': 'Suggestion deleted successfully'}), 203
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gateway_service.route('/create_entry', methods=['PUT'])
@token_required(allowed_roles=[1, 2])
def create_entry(payload):
    category = request.json.get('category')
    title = request.json.get('title')
    description = request.json.get('description')

    if not category or not title or not description:
        return jsonify({'error': 'Missing category, title, or description!'}), 406

    try:
        crud_services.create_entry(category, title, description)
        return jsonify({'message': 'Suggestion added successfully'}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gateway_service.route('/get_suggestion', methods=['GET'])
def get_suggestion():
    try:
        suggestion = crud_services.random_entry()
        if suggestion:
            return jsonify({
                'category': suggestion[0],
                'title': suggestion[1],
                'description': suggestion[2]
            })
        else:
            return jsonify({'error': 'No suggestions found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Registration Endpoint
@gateway_service.route('/register-user', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_auth.insert_user_cred(username, hashed_password)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Login Endpoint
@gateway_service.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        user_info = user_auth.get_user_info(username)
        if user_info and bcrypt.checkpw(password.encode('utf-8'), user_info[1].tobytes()):
            payload = {
                'user': username,
                'rank': user_info[2],
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }
            token = jwt.encode(payload, gateway_service.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    gateway_service.run(debug=True, port=5000)
