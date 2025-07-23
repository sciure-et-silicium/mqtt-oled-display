from .configuration import Configuration
from .display_item import DisplayItem
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from . import db  

Base = declarative_base()

def init_database(app=None):
    if app is not None:
        _init_flask_db(app)
    else :
        _init_standalone_db()

def _init_flask_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    with app.app_context():
        db.init_app(app)
        db.create_all()
        init_default_config()
        init_sample_data()

def _init_standalone_db():
    engine = create_engine('sqlite:///./instance/database.db')
    Base.metadata.bind = engine

    # Configure session
    Session = orm.scoped_session(orm.sessionmaker(bind=engine))
    db.session = Session

    # Make db.Model work like in Flask-SQLAlchemy
    db.Model = Base
    db.Column = db.Column
    db.relationship = orm.relationship
    db.ForeignKey = db.ForeignKey

    # Create tables
    Base.metadata.create_all(engine)

    init_default_config()
    init_sample_data()

def init_default_config():
    defaults = {
        'mqtt.broker': ('localhost', 'MQTT broker address'),
        'mqtt.port': ('1883', 'Port du broker MQTT'),
        'mqtt.username': ('', 'MQTT username'),
        'mqtt.password': ('', 'MQTT password'),
        'mqtt.keepalive': ('60', ''),
        'mqtt.qos': ('1', ''),
        'mqtt.client_id': ('data_collector', 'MQTT client id')
    }
    
    for key, (value, description) in defaults.items():
        if not Configuration.query.filter_by(key=key).first():
            config = Configuration(key=key, value=value, description=description)
            db.session.add(config)
            db.session.commit()
            

def init_sample_data():
    if DisplayItem.query.count() == 0:
        samples = [
            DisplayItem(name='Living Room Temperature', mqtt_topic='sensors/living_room/temperature', render_template='{{payload.temperature}}°C', display_order=1, duration=5),
            DisplayItem(name='Humidity Living Room', mqtt_topic='sensors/living_room/humidity', render_template='{{payload.humidity}}%', display_order=2, duration=5),
            DisplayItem(name='Kitchen Temperature', mqtt_topic='sensors/kitchen/temperature', render_template='{{payload.temperature}}°C', display_order=3, duration=5),
        ]
        
        for item in samples:
            db.session.add(item)
        db.session.commit()
