# api/config.py
from flask import Blueprint, request, jsonify
from database import db, Configuration

api_config = Blueprint('api_config', __name__, url_prefix="/api/config")

@api_config.route('', methods=['GET'])
def get_all():
    items = Configuration.get_all()
    return jsonify([item.to_dict() for item in items])

@api_config.route('/<string:key>', methods=['GET'])
def get_item(key):
    try:
        item = Configuration.query.get_or_404(key)
        return jsonify(item.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_config.route('/<string:key>', methods=['PUT'])
def update_item(key):
    try:
        item = Configuration.query.get_or_404(key)
        data = request.get_json()

        if not data.get('value'):
            return jsonify({'error': 'value is required'}), 400
        
        item.value = data['value']
        item.description = data.get('description', item.description)
        
        db.session.commit()
        
        return jsonify(item.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500