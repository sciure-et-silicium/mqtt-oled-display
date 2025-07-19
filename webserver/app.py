# app.py
from flask import Flask
from database import db, init_database

# Import des blueprints
from api import api_config, api_display_item
from web.routes import web_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre-cle-secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Enregistrement des blueprints
app.register_blueprint(api_config)
app.register_blueprint(api_display_item)

app.register_blueprint(web_bp)

@app.before_first_request
def create_tables():
    init_database()

if __name__ == '__main__':
    with app.app_context():
        init_database()
    
    app.run(debug=True, port=5000, host='0.0.0.0')
