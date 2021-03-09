from flask import Blueprint

bp = Blueprint('courses', __name__)

from app.courses import routes, services, models