import os
from dotenv import load_dotenv

dotenv_path = os.path.join(
    os.path.dirname(__file__),
    '.env'
)

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from app import create_app, db, User, Course
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Course': Course
    }
