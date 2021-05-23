from . import bp as projects
from flask import render_template, current_app, redirect, request
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError, OperationFailure
from pymongo import ReturnDocument
from app.utils import success, error
from .sheets import sheets_team_add_member
from app.models import Project, User
from app.utils import required_json_arguments
from mongoengine import DoesNotExist
from app.projects.services import get_project_table
from mongoengine import signals
import json


@projects.route('/')
@projects.route('/index')
@login_required
def index():
    projects = Project.objects.filter(disabledForJoin=False).exclude('teams.members')

    already_joined_project = Project.objects.filter(teams__members__in=[current_user]).first()

    return render_template(
        'projects/index.html',
         projects=projects,
         user=current_user,
         already_joined_project=already_joined_project
    )


@projects.route('/api/<id>/', methods=['GET'])
@login_required
def projects_get(id: str):
    try:
        doc = Project.objects.get(id=id)
        return success('found', data=json.loads(doc.to_json()))
    except DoesNotExist:
        return error(f'Project with ID {id} does not exist', status_code=404)


@projects.route('/api/find/<query>', methods=['GET'])
@login_required
def get_project_by_name(query: str):
    try:
        doc = Project.objects.get(name__icontains=query)
        return success('found', data=json.loads(doc.to_json()))
    except DoesNotExist:
        return error('Project with such name does not exist', status_code=404)

@projects.route('/api/available', methods=['GET'])
@login_required
def check_project_availability():
    docs = Project.objects.filter(disabledForJoin=False).exclude('teams.members')
    return success('available', data=[json.loads(d.to_json()) for d in docs])

@projects.route('/api/<id>/join', methods=['POST'])
@required_json_arguments
@login_required
def join_project(id: str, team_number: str):
    already_joined = Project.objects.filter(teams__members__in=[current_user]).first()
    if already_joined is not None:
        return error(f'Вы уже записаны на проект "{already_joined.name}"!')

    if current_user.role != 'Студент':
        return error('На проект могут записаться только студенты!', status_code=409)

    try:
        project = Project.objects.get(id=id)
        rv = project.update(
            **{f'push__teams__{team_number}__members': current_user}
        )
        if rv:
            project.save()
            return success(f'Вы успешно записаны на проект', data={})
        else:
            return error('При записи произошла неизвестная ошибка!', status_code=500)
    except DoesNotExist:
        return error(f'No project with ID {id}', status_code=404)


@projects.route('/table', methods=['GET'])
@login_required
def get_table():
    data = get_project_table()
    return render_template('projects/accordion.html', data=data)