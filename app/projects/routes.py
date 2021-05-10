from . import bp as projects
from flask import render_template, current_app, redirect, request


@projects.route('/')
@projects.route('/index')
def index():
    return render_template('projects/index.html')