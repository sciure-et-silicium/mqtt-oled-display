from . import db

class DisplayItem(db.Model):
    __tablename__ = 'display_item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mqtt_topic = db.Column(db.String(255), nullable=False)
    render_template = db.Column(db.String(255), nullable=False) 
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
            'render_template': self.render_template,
            'duration': self.duration,
            'display_order': self.display_order,
            'is_active': self.is_active
        }
    
    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.display_order, cls.name).all()

    # use thread safe session for this method
    @classmethod
    def get_all_active(cls):
        session = db.session()  
        try:
            return session.query(cls).filter_by(is_active=True).order_by(cls.display_order, cls.mqtt_topic).all()
        finally:
            session.close()  