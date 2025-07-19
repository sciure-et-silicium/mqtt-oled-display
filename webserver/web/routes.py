from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import DisplayItem, Configuration

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def display_items():
    items = DisplayItem.get_all()
    return render_template('display_items.html', items=items)

@web_bp.route('/config')
def config_page():
    configurations = Configuration.get_all()
    return render_template('config.html', configurations=configurations)
