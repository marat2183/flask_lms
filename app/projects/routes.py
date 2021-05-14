from . import bp as projects
from flask import render_template, current_app, redirect, request
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError, OperationFailure
from pymongo import ReturnDocument
from app.utils import success, error
from .sheets import sheets_team_add_member
from app.models import Project, User
from mongoengine import DoesNotExist
from mongoengine import signals
import json


@projects.route('/')
@projects.route('/index')
@login_required
def index():
    projects = Project.objects()
    return render_template('projects/index.html', projects=projects, user=current_user)


@projects.route('/api/projects/<id>/', methods=['GET'])
@login_required
def projects_get(id: str):
    try:
        doc = Project.objects.get(id=id)
        return success('found', data=json.loads(doc.to_json()))
    except DoesNotExist:
        return error(f'Project with ID {id} does not exist', status_code=404)



@projects.route('/api/projects/find/<query>', methods=['GET'])
@login_required
def get_by_name_proj(query: str):
    try:
        doc = Project.objects.get(name__icontains=query)
        return success('found', data=json.loads(doc.to_json()))
    except DoesNotExist:
        return error('Project with such name does not exist', status_code=404)



@projects.route('/api/projects/<id>/available', methods=['GET'])
@login_required
def check_project_availability(id: str):
    try:
        docs = Project.objects.get(available=True)
        return success('available', data=[json.loads(d.to_json()) for d in docs])
    except DoesNotExist:
        return error('No project with such ID', status_code=404)

@projects.route('/api/projects/<id>/teams', methods=['GET'])
@login_required
def get_project_teams(id: str):
    try:
        doc = Project.objects.get(id=id)
        return success('teams for project', data=json.loads(doc.teams.to_json()))
    except DoesNotExist:
        return error(f'No project with ID {id}', status_code=404)


@projects.route('/api/projects/<id>/join', methods=['POST', 'PUT'])
@login_required
def join_project(id: str, name: str, group: str, team: str):
    if len(Project.objects(teams__members__name=name)) >= 1:
        return error('Вы уже записаны на проект')

    if current_user.role != 'Студент':
        return error('На проект могут быть записаны только студенты!', status_code=409)

    try:
        Project.objects.find(id=id).update_one(push__teams__S__members=current_user)
        return success(f'Вы успешно записаны ны проект', data={})
    except DoesNotExist:
        return error(f'No project with ID {id}', status_code=404)
