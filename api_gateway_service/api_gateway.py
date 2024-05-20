import sys
import os
from flask import Flask, request, jsonify
import requests
import jwt
from functools import wraps

sys.path.append(r"C:\Users\Kevin\Desktop\bored_microservice")
import suggestion-service
print(sys.path)
print(suggestion-service)



auth_service = Flask(__name__)
auth_service.config['SECRET_KEY'] = '5f4102db508e4065ace3df7ae799f6cf'


def token_required(allowed_roles):
    """Check for jws"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'Alert!': 'Token is missing!'}), 403

            try:
                payload = jwt.decode(token.split(" ")[1], auth_service.config['SECRET_KEY'], algorithms=['HS256'])
                if payload['rank'] not in allowed_roles:
                    return jsonify({'error': 'Access denied!'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'Alert!': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'Alert!': 'Invalid Token!'}), 401

            return f(payload, *args, **kwargs)

        return wrapper

    return decorator
