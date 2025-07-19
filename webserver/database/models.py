# database/models.py
from datetime import datetime
from . import db

class DisplayItem(db.Model):
    __tablename__ = 'display_item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mqtt_topic = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(20))
    duration = db.Column(db.Integer, default=0)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<DisplayItem {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mqtt_topic': self.mqtt_topic,
            'unit': self.unit,
            'duration': self.duration,
            'display_order': self.display_order,
            'is_active': self.is_active
        }
    
    @classmethod
    def get_all(cls):
        """Retourne les items actifs triés par ordre d'affichage"""
        return cls.query.order_by(cls.display_order, cls.name).all()
    
    @classmethod
    def get_all_topics(cls):
        """Retourne tous les topics MQTT actifs"""
        return [item.mqtt_topic for item in cls.get_all()]

class Configuration(db.Model):
    __tablename__ = 'configuration'
    
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Configuration {self.key}={self.value}>'
    
    def to_dict(self):
        return {
            'key': self.key,
            'value': self.value,
            'description': self.description
        }

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.key).all()
