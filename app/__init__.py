import os
from flask import Flask
from config import Configuration
from app.auth import bp as auth_bp
from app.courses import bp as courses_bp
from flask import session
import flask_admin as admin
from .courses.models import *
from flask_babelex import Babel
# from .courses import bp as courses_blueprint
# from .auth import bp as auth_bp
import mongoengine as db
from .courses.admin_views import *



app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
    return 'ru'


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





admin = admin.Admin(app, name='Flaks_lms', template_mode='bootstrap4')

admin.add_view(TeacherView(TeacherUser, name='Учителя'))
admin.add_view(StudentView(StudentUser, name='Студенты'))
admin.add_view(CourseView(Course, name='Курсы'))
admin.add_view((GroupView(Group, name='Группы')))
admin.add_view(AuditoriumView(Auditorium, name='Аудитории'))

app.register_blueprint(auth_bp, url_prefix='/auth')

app.register_blueprint(courses_bp, url_prefix='/courses')

from app import routes
