from app import app
from flask import request
from flask import render_template





@app.route('/')
@app.route('/index')
def index():
    return 'Hello'


