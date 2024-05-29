import sys
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from suggestion_service import crud_services
import jwt
from functools import wraps
from auth_service import user_auth
import bcrypt

#logging
from logging_service import logger_sender
logger = logger_sender.configure_logging('api_gateway',fluentd_host='fluentd', fluentd_port=24224)

#Testing
from testing_service import microservice_test


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
                logger.info("Missing JWT Token.")
                return jsonify({'Alert!': 'Token is missing!'}), 403

            try:
                payload = jwt.decode(token.split(" ")[1], gateway_service.config['SECRET_KEY'], algorithms=['HS256'])
                if payload['rank'] not in allowed_roles:
                    logger.info("Tried to access wrong role/ No perms. ")
                    return jsonify({'error': 'Access denied!'}), 403
            except jwt.ExpiredSignatureError:
                logger.info("Token expired.")
                return jsonify({'Alert!': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                logger.info("Wrong/Invalid Token.")
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
        logger.info("Unable to delete suggestion. Missing Category, title or description")
        return jsonify({'error': 'Missing category, title, or description!'}), 406

    try:
        crud_services.delete_entry(category, title, description)
        logger.error(f"Api_Gateway: {category}, {title}, {description} when deleting. ")
        return jsonify({'message': 'Suggestion deleted successfully'}), 203
    except Exception as e:
        logger.error(f"Api_Gateway: Exception of {e} when deleting suggestions")
        return jsonify({'error': str(e)}), 500

@gateway_service.route('/create_entry', methods=['PUT'])
@token_required(allowed_roles=[1, 2])
def create_entry(payload):
    category = request.json.get('category')
    title = request.json.get('title')
    description = request.json.get('description')

    if not category or not title or not description:
        logger.info("Unable to create suggestion. Missing Category, title or description")
        return jsonify({'error': 'Missing category, title, or description!'}), 406

    try:
        crud_services.create_entry(category, title, description)
        logger.error(f"Api_Gateway: {category}, {title}, {description} while creating. ")
        return jsonify({'message': 'Suggestion added successfully'}), 202
    except Exception as e:
        logger.error(f"Api_Gateway: Exception of {e} when creating suggestions")
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
            logger.error(f"Api_gateway: No suggestion found")
            return jsonify({'error': 'No suggestions found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Registration Endpoint
@gateway_service.route('/register-user', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        logger.warning("Register error, username or password missing")
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_auth.insert_user_cred(username, hashed_password)
        logger.info(f"User successfully registered with the user {username}")
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        logger.error(f"exception when trying to register {e}")
        return jsonify({'error': str(e)}), 500

# Login Endpoint
@gateway_service.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        logger.warning("Login error, username or password missing")
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
            logger.info("Login success, jwt token sent.")
            return jsonify({'token': token}), 200
        else:
            logger.error("Login failed. Wrong password or username.")
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        logger.error(f"login failed {e} exception")
        return jsonify({'error': str(e)}), 500


@gateway_service.route('/admin-test', methods=['GET'])



if __name__ == '__main__':
    gateway_service.run(debug=True, port=5000)
