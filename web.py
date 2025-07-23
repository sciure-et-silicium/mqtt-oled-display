from flask import Flask
from database import db, init_database

# Import blueprints
from web.api import api_config, api_display_item, api_render_preview
from web.web.routes import web_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.template_folder = 'web/templates'
app.static_folder = 'web/static'     # Pour les fichiers statiques
app.static_url_path = '/static'      # URL de base pour les fichiers statiques

init_database(app)

# Blueprint registration
app.register_blueprint(api_config)
app.register_blueprint(api_display_item)
app.register_blueprint(api_render_preview)
app.register_blueprint(web_bp)

app.run(debug=True, port=5000, host='0.0.0.0')