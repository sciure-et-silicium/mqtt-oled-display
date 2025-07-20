from flask import Blueprint, request, jsonify
from database import db, DisplayItem, Configuration

api_display_item = Blueprint('api_display_item', __name__, url_prefix="/api/display_item")

@api_display_item.route('', methods=['GET'])
def get_all():
    items = DisplayItem.get_all()
    return jsonify([item.to_dict() for item in items])

@api_display_item.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = DisplayItem.query.get_or_404(item_id)
        return jsonify(item.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_display_item.route('', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('mqtt_topic'):
            return jsonify({'error': 'Name and MQTT topic are required'}), 400
        
        existing = DisplayItem.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Name already exists'}), 400
        
        item = DisplayItem(
            name=data['name'],
            mqtt_topic=data['mqtt_topic'],
            render_template=data.get('render_template', ''),
            display_order=data.get('display_order', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(item.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_display_item.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        item = DisplayItem.query.get_or_404(item_id)
        data = request.get_json()
        
        if not data.get('name') or not data.get('mqtt_topic'):
            return jsonify({'error': 'Name and MQTT topic are required'}), 400
        
        existing = DisplayItem.query.filter(
            DisplayItem.name == data['name'],
            DisplayItem.id != item_id
        ).first()
        if existing:
            return jsonify({'error': 'Name already exists'}), 400

        item.name = data['name']
        item.mqtt_topic = data['mqtt_topic']
        item.render_template = data.get('render_template', '')
        item.display_order = data.get('display_order', 0)
        item.is_active = data.get('is_active', True)
        
        db.session.commit()
        
        return jsonify(item.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_display_item.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        item = DisplayItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
