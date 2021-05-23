import os
from dotenv import load_dotenv

dotenv_path = os.path.join(
    os.path.dirname(__file__),
    '.env'
)

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from app import create_app, db, oauth
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
from app.models import User, Project, Course, Auditorium, Group

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'oauth': oauth,
        'User': User,
        'Course': Course,
        'Group': Group,
        'Project': Project,
        'Auditorium': Auditorium
    }
