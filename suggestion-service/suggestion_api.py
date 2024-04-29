from flask import Flask, request, jsonify
from crud_services import get_db_connection,create_entry,delete_entry,random_entry

suggesion_microservice = Flask(__name__)



@suggesion_microservice.route('/create', methods=['POST'])
def create_suggestion():
    pass



@suggesion_microservice.route('/random', methods=['GET'])
def random_suggestion():
    pass