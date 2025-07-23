from . import db  

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

    @classmethod
    def get_value_by_key(cls, key):
        config = cls.query.filter_by(key=key).first()
        return config.value if config else None
        