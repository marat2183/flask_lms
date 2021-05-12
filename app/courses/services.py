from bson.objectid import ObjectId
from app.models import Course
from mongoengine.errors import OperationError


def get_courses_by_id(id) -> dict:
    try:
        courses = Course.objects().aggregate(
        [
            {
                '$match': {
                  '_id': ObjectId(id)
                }
            },
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'teachers',
                    'foreignField': '_id',
                    'as': 'teachers'
                }
            },
            # {
            #     '$lookup': {
            #         'from': 'auditorium',
            #         'localField': 'labs_auds',
            #         'foreignField': '_id',
            #         'as': 'labs_auds'
            #     }
            # },
            {
                '$lookup': {
                    'from': 'auditorium',
                    'localField': 'lectures_auds',
                    'foreignField': '_id',
                    'as': 'lectures_auds'
                }
            },
            # {
            #     '$lookup': {
            #         'from': 'auditorium',
            #         'localField': 'practice_auds',
            #         'foreignField': '_id',
            #         'as': 'practice_auds'
            #     }
            # },
            {
                '$lookup': {
                    'from': 'course',
                    'localField': 'links',
                    'foreignField': '_id',
                    'as': 'links'
                }
            }
        ]
        )
        return list(courses)[0]
    except OperationError:
        return dict()
    except:
        return dict()


def get_courses_able_to_join(id):
    try:
        courses = Course.objects(students__nin=[id], archived=False)
        return list(courses)
    except OperationError:
        return []
    except:
        return []


def get_user_courses(id):
    try:
        courses = Course.objects(students__in=[id], archived=False)
        return list(courses)
    except OperationError:
        return []
    except:
        return []


def join_to_course(user_id, course_id):
    try:
        Course.objects(id=course_id).update_one(push__students=user_id)
        return True
    except OperationError:
        return False
    except:
        return False




