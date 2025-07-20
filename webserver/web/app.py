# web/app.py
from flask import Flask
from database import db, init_database

# Import blueprints
from .api import api_config, api_display_item, api_render_preview
from .web.routes import web_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'verysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Database initialization
    db.init_app(app)

    # Blueprint registration
    app.register_blueprint(api_config)
    app.register_blueprint(api_display_item)
    app.register_blueprint(api_render_preview)
    app.register_blueprint(web_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        init_database()
    
    app.run(debug=True, port=5000, host='0.0.0.0')