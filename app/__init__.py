import os
from flask import Flask
from config import Configuration
from app.auth import bp as auth_bp
from app.courses import bp as courses_bp
from flask import session
import flask_admin as admin
from flask_admin.form import Select2Widget
from flask_admin.contrib.mongoengine import ModelView
from .courses.models import *
# from .courses import bp as courses_blueprint
# from .auth import bp as auth_bp
import mongoengine as db

app = Flask(__name__)
app.config.from_object(Configuration)
db_name = app.config['DB_NAME']
db_username = app.config['DB_USERNAME']
db_password = app.config['DB_PASSWORD']
DB_URL = 'mongodb+srv://{}:{}@cluster0.k1li3.mongodb.net/{}?retryWrites=true&w=majority'.format(
    db_username,
    db_password,
    db_name
)
db.connect(host=DB_URL)


admin = admin.Admin(app)
admin.add_view(ModelView(TeacherUser, name='Teachers'))
admin.add_view(ModelView(StudentUser, name='Students'))
admin.add_view(ModelView(Coursetest, name='Courses'))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(courses_bp, url_prefix='/courses')


from app import routes