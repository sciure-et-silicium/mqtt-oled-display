# database/init_db.py
from . import db
from .models import DisplayItem, Configuration

def init_database():
    """Initialise la base de données"""
    db.create_all()
    init_default_config()
    init_sample_data()

def init_default_config():
    """Initialise la configuration par défaut"""
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
    """Initialise des données d'exemple (optionnel)"""
    if DisplayItem.query.count() == 0:
        samples = [
            DisplayItem(name='Température Salon', mqtt_topic='sensors/salon/temperature', unit='°C', display_order=1, duration=5),
            DisplayItem(name='Humidité Salon', mqtt_topic='sensors/salon/humidity', unit='%', display_order=2, duration=5),
            DisplayItem(name='Température Chambre', mqtt_topic='sensors/chambre/temperature', unit='°C', display_order=3, duration=5),
        ]
        
        for item in samples:
            db.session.add(item)
        db.session.commit()
