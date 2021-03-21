from flask import Flask
from config import Config
import flask_admin as admin
from flask_babelex import Babel
from flask_session import Session
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_mongoengine import MongoEngine


babel = Babel()

@babel.localeselector
def get_locale():
    return 'ru'


oauth = OAuth()
sess = Session()
login_manager = LoginManager()

db = MongoEngine()

admin = admin.Admin(name='Flask_lms', template_mode='bootstrap4')


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    sess.init_app(app)
    babel.init_app(app)
    oauth.init_app(app)
    db.init_app(app)

    admin.init_app(app)

    login_manager.init_app(app)

    # к экземляру клиента OAuth можно обращаться из любой точки приложения через oauth.azure.<method_name>
    tenant_name = app.config.get('AZURE_TENANT_NAME')

    from models import fetch_azure_token, update_azure_token

    oauth.register(
        name='azure',
        client_id=app.config.get('AZURE_CLIENT_ID'),
        client_secret=app.config.get('AZURE_CLIENT_SECRET'),
        client_kwargs={
            'scope': 'offline_access email profile openid User.Read.All',
            'token_endpoint_auth_method': 'client_secret_basic',
            'token_placement': 'header'
        },
        api_base_url=app.config.get('AZURE_API_BASE_URL'),
        access_token_method='POST',
        server_metadata_url=f'https://login.microsoftonline.com/{tenant_name}/v2.0/.well-known/openid-configuration',
        fetch_token=fetch_azure_token,
        update_token=update_azure_token
    )

    from models import TeacherUser, Course, Group, Auditorium, User, load_user
    from courses.admin_views import TeacherView, StudentView, CourseView, AuditoriumView, GroupView

    admin.add_view(TeacherView(TeacherUser, name='Учителя'))
    admin.add_view(StudentView(User, name='Студенты'))
    admin.add_view(CourseView(Course, name='Курсы'))
    admin.add_view((GroupView(Group, name='Группы')))
    admin.add_view(AuditoriumView(Auditorium, name='Аудитории'))

    from .auth import bp as auth_bp
    from .courses import bp as courses_bp
    from .main import bp as main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(main_bp, url_prefix='/')

    login_manager.user_loader(load_user)

    return app