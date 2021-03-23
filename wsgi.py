import os
from dotenv import load_dotenv

dotenv_path = os.path.join(
    os.path.dirname(__file__),
    '.env'
)

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from app import create_app, db, oauth, User, Course
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'oauth': oauth,
        'User': User,
        'Course': Course
    }
