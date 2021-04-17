from bson.objectid import ObjectId
from app.models import Course


def get_courses_by_id(id) -> Course:
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
        }
    ]
)
    return list(courses)[0]


def get_courses_able_to_join(id):
    courses = Course.objects(students__nin=[id])
    return list(courses)


def get_user_courses(id):
    courses = Course.objects(students__in=[id])
    return list(courses)



