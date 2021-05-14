from typing import Union, List, Dict, Optional, Tuple
from pymongo.errors import OperationFailure, PyMongoError
from bson.objectid import ObjectId
from app.utils import success, error
from app.models import Project
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
