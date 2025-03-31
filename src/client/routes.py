from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from extensions import db  # Importa db desde extensions.py
from models.blacklist import Blacklist
import datetime
import re

# Crear un Blueprint para las rutas de blacklist
routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/login', methods=['GET'])
def login():
    static_token = create_access_token(identity='static-user', expires_delta=False)
    return jsonify({'token': static_token}), 200

@routes_bp.route('/blacklists', methods=['POST'])
@jwt_required()
def add_to_blacklist():
    data = request.get_json()

    required_fields = ['email', 'app_uuid', 'blocked_reason']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({'message': f'El campo "{field}" es obligatorio y no puede estar vacío'}), 400

    email = data.get('email').strip()
    app_uuid = data.get('app_uuid').strip()
    blocked_reason = data.get('blocked_reason', '').strip()

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return jsonify({'message': 'Formato de email inválido'}), 400

    uuid_regex = r'^[a-fA-F0-9-]{36}$'
    if not re.match(uuid_regex, app_uuid):
        return jsonify({'message': 'Formato de UUID inválido'}), 400

    is_blacklisted = Blacklist.query.filter_by(email=email).first()
    if is_blacklisted:
        return jsonify({'message': 'Email ya está en la lista negra'}), 400

    record = Blacklist(
        email=email,
        app_uuid=app_uuid,
        blocked_reason=blocked_reason,
        ip_address=request.remote_addr,
        timestamp=datetime.datetime.now()
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({'message': 'Email agregado a la lista negra'}), 201

@routes_bp.route('/blacklists/<string:email>', methods=['GET'])
@jwt_required()
def check_blacklist(email):
    email = email.strip()
    record = Blacklist.query.filter_by(email=email).first()

    if record:
        return jsonify({
            'blacklisted': True,
            'blocked_reason': record.blocked_reason
        }), 200
    else:
        return jsonify({'blacklisted': False}), 200
