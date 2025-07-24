from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import DisplayItem

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def display_items():
    items = DisplayItem.get_all()
    return render_template('display_items.html', items=items)
