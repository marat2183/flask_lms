from . import bp as projects
from flask import render_template, current_app, redirect, request
from flask_login import login_required


@projects.route('/')
@projects.route('/index')
@login_required
def index():
    return render_template('projects/index.html')