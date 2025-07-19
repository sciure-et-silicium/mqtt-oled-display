# database/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Instance globale SQLAlchemy
db = SQLAlchemy()

# Imports pour faciliter l'utilisation
from .models import DisplayItem, Configuration
from .connection import get_db_connection
from .init_db import init_database, init_default_config

__all__ = [
    'db',
    'DisplayItem', 
    'Configuration',
    'get_db_connection',
    'init_database',
    'init_default_config'
]
