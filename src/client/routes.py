from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from app import app, db
from models import *
import uuid

# Endpoint para agregar un email a la lista negra
@app.route('/blacklists', methods=['POST'])
#@jwt_required()
def add_to_blacklist():

    return jsonify({'message': 'Email agregado a la lista negra'}), 201

# Endpoint para verificar si un email está en la lista negra
@app.route('/blacklists/<string:email>', methods=['GET'])
@jwt_required()
def check_blacklist(email):
   
    return jsonify({'blacklisted': False}), 200


