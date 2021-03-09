import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
cluster = MongoClient('mongodb+srv://test_user:passwordistestuser@cluster0.k1li3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['flask_project']
students_collection = db['students']
teachers_collection = db['teachers']
courses_collection = db['courses']

def get_courses_by_id(id):
    courses = courses_collection.aggregate(
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
    courses = courses_collection.find({'groups': group}, {'name': 1, 'description': 1})
    return list(courses)



