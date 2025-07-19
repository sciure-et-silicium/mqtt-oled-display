# database/init_db.py
from . import db
from .configuration import Configuration
from .display_item import DisplayItem


def init_database():
    db.create_all()
    init_default_config()
    init_sample_data()

def init_default_config():
    defaults = {
        'mqtt.broker': ('localhost', 'Adresse du broker MQTT'),
        'mqtt.port': ('1883', 'Port du broker MQTT'),
        'mqtt.username': ('', 'Nom d\'utilisateur MQTT'),
        'mqtt.password': ('', 'Mot de passe MQTT'),
        'mqtt.keepalive': ('60', 'Keepalive MQTT en secondes'),
        'mqtt.qos': ('1', 'QoS MQTT (0, 1 ou 2)'),
        'mqtt.client_id': ('data_collector', 'ID du client MQTT')
    }
    
    for key, (value, description) in defaults.items():
        if not Configuration.query.filter_by(key=key).first():
            config = Configuration(key=key, value=value, description=description)
            db.session.add(config)
            db.session.commit()
            

def init_sample_data():
    if DisplayItem.query.count() == 0:
        samples = [
            DisplayItem(name='Living Room Temperature', mqtt_topic='sensors/living_room/temperature', unit='°C', display_order=1, duration=5),
            DisplayItem(name='Humidity Living Room', mqtt_topic='sensors/living_room/humidity', unit='%', display_order=2, duration=5),
            DisplayItem(name='Kitchen Temperature', mqtt_topic='sensors/kitchen/temperature', unit='°C', display_order=3, duration=5),
        ]
        
        for item in samples:
            db.session.add(item)
        db.session.commit()
