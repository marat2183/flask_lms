from app.auth import bp as auth_bp
from flask import render_template



@auth_bp.route('/')
def index():
    return render_template(template_name_or_list='auth/login.html')


