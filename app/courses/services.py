from bson.objectid import ObjectId
from models import Course


def get_courses_by_id(id):
    courses = Course.objects().aggregate(
    [
        {
            '$match': {
              '_id': ObjectId(id)
            }
        },
        {
            '$lookup': {
                'from': 'teachers',
                'localField': 'teachers',
                'foreignField': '_id',
                'as': 'teachers'
            }
        }
    ]
)
    return list(courses)[0]


def get_courses_by_group(group):
    courses = Course.objects(groups=group)
    # courses = Course.objects.find({'groups': group}, {'name': 1, 'description': 1})
    return list(courses)



