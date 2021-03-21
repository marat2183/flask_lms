from . import bp as main
from flask import render_template, current_app, redirect, request
from flask_login import current_user

@main.route('/')
@main.route('/index')
def index():
    return 'Hello'