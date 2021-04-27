from bson.objectid import ObjectId
from app.models import Course
from mongoengine.errors import OperationError


def get_courses_by_id(id) -> Course:
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
            {
                '$lookup': {
                    'from': 'auditorium',
                    'localField': 'labs_auds',
                    'foreignField': '_id',
                    'as': 'labs_auds'
                }
            },
            {
                '$lookup': {
                    'from': 'auditorium',
                    'localField': 'lectures_auds',
                    'foreignField': '_id',
                    'as': 'lectures_auds'
                }
            },
            {
                '$lookup': {
                    'from': 'auditorium',
                    'localField': 'practice_auds',
                    'foreignField': '_id',
                    'as': 'practice_auds'
                }
            },
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
        pass
    except:
        pass


def get_courses_able_to_join(id):
    try:
        courses = Course.objects(students__nin=[id])
        return list(courses)
    except OperationError:
        pass
    except:
        pass

def get_user_courses(id):
    try:
        courses = Course.objects(students__in=[id])
        return list(courses)
    except OperationError:
        pass
    except:
        pass


def join_to_course(user_id, course_id):
    try:
        Course.objects(id=course_id).update_one(push__students=user_id)
    except OperationError:
        pass
    except:
        pass
    return True



