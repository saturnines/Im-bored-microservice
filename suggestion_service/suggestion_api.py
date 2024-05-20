from flask import Flask, request, jsonify
from crud_services import get_db_connection,create_entry,delete_entry,random_entry

suggesion_microservice = Flask(__name__)

get_db_connection()

@suggesion_microservice.route('/suggestion', methods=['POST'])
def create_suggestion():
    if not request.json or not 'category' in request.json or not 'title' in request.json:
        return jsonify({'error': 'Missing required fields'}), 400 #return if not found

    category = request.json['category']
    title = request.json['title']
    description = request.json.get('description', '')

    try:
        create_entry(category, title, description)
        return jsonify({'message': 'Suggestion created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@suggesion_microservice.route('/delete', methods=['POST'])
def delete_suggestion():
    """Delete portion of the API."""
    if not request.json or not 'category' in request.json or not 'title' in request.json or not 'description' in request.json:
        return jsonify({'error': 'Missing required fields'}), 400 #return if not found

    category = request.json['category']
    title = request.json['title']
    description = request.json.get('description', '')

    try:
        delete_entry(category, title, description)
        return jsonify({'message': 'Suggestion deleted successfully'}), 201
    except Exception as e:
        return jsonify({'error':str(e)}), 500


@suggesion_microservice.route('/random', methods=['GET'])
def random_suggestion():
    try:
        result = random_entry()
        if result is None:
            return jsonify({'error':' No Suggestions available'}), 404 # return error if there's nothing in the DB.

        return jsonify({'category': result[0], 'title': result[1], 'description': result[2]}), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 500
