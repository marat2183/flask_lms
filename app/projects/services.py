from typing import Union, List, Dict, Optional, Tuple
from pymongo.errors import OperationFailure, PyMongoError
from bson.objectid import ObjectId
from app.utils import success, error
from app.models import Project, User
from mongoengine import DoesNotExist


def get_project_by_id(id: str) -> Dict:
    try:
        proj = Project.objects.get(id=id)
    except DoesNotExist as e:
        return error('Проект не найден')

    return proj.to_json()


def get_project_by_name(query: str) -> Dict:
    try:
        doc = Project.objects.get(name=query)
    except DoesNotExist as e:
        return error('not found', status_code=404)

    return doc.to_json()


def get_project_table():
    results = []
    a = User.objects.filter(is_mentor=True)
    for user in a:
        temp = dict()
        temp['mentor'] = user.fullname
        proj = Project.objects(mentor=user.id)
        temp['projects'] = []
        for project in proj:
            test = Project.objects().aggregate(
                [
                    {
                        '$match': {
                            '_id': ObjectId(project.id)
                        }
                    },
                    {
                        '$unwind': "$teams"
                    },
                    {
                        '$lookup': {
                            'from': 'user',
                            'localField': 'teams.members',
                            'foreignField': '_id',
                            'as': 'teams.members'
                        }
                    },
                    {
                        "$project": {
                            "name": 1,
                            "teams.members.fullname": 1,
                        }
                    }

                ]
            )
            t = list(test)
            temp_dict = {}
            temp_dict['name'] = project.name
            temp_dict['members'] = t
            temp['projects'].append(temp_dict)
        results.append(temp)
    return results