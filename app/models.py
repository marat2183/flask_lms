import mongoengine as db
from flask_login import UserMixin
from flask import url_for, current_app
from jinja2 import Markup
from flask_admin.form import DatePickerWidget
from flask_admin.form.widgets import DatePickerWidget
from mongoengine import CASCADE, PULL
from mongoengine import signals
from bson import json_util
import requests
import os

def fetch_azure_token(request):
    token = OAuth2Token.objects(name='azure', user=request.user)
    return token


def update_azure_token(name, token, refresh_token=None, access_token=None):
    if refresh_token:
        item = OAuth2Token.objects(name=name, refresh_token=refresh_token)
    elif access_token:
        item = OAuth2Token.objects(name=name, access_token=access_token)
    else:
        return
    # update old token
    item.access_token = token['access_token']
    item.refresh_token = token.get('refresh_token')
    item.expires_at = token['expires_at']
    item.save()


class Group(db.Document):
    name = db.StringField()

    def __unicode__(self):
        return self.name


class Auditorium(db.Document):
    name = db.StringField()

    def __unicode__(self):
        return self.name


class Theme(db.EmbeddedDocument):
    name = db.StringField()
    description = db.StringField()
    # start_date = db.DateTimeField()
    # end_date = db.DateTimeField()

    def __unicode__(self):
        return self.name


class OAuth2Token(db.EmbeddedDocument):
    name = db.StringField()
    scope = db.StringField()
    token_type = db.StringField()
    access_token = db.StringField()
    refresh_token = db.StringField()
    id_token = db.StringField()
    expires_in = db.IntField()
    ext_expires_in = db.IntField()
    expires_at = db.IntField()

    def __unicode__(self):
        return f'<{self.name}>'


class User(UserMixin, db.Document):
    active = db.BooleanField(default=True)
    azure_oid = db.UUIDField(binary=False)

    token = db.EmbeddedDocumentField(OAuth2Token)

    role = db.StringField(choices=["Студент", "Преподаватель", "Администратор"])

    email = db.EmailField(allow_utf8_user=True)

    fullname = db.StringField()
    group = db.ReferenceField(Group)
    description = db.StringField()
    # courses = db.ListField(db.ReferenceField(Course))

    def __unicode__(self):
        return self.fullname

    def get_id(self):
        return str(self.pk)

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data.pop('token', None)
        return json_util.dumps(data)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if document.role == 'Студент':
            if not document.email:
                return
            response = requests.get(
                os.environ.get('ICTIS_API_URL'),
                auth=(os.environ.get('ICTIS_API_LOGIN'), os.environ.get('ICTIS_API_PASSWORD')),
                params={'email': document.email}
            )
            response.raise_for_status()
            data = response.json().get('student')
            if not data:
                return
            group = 'КТ{}{}-{}{}'.format(
                data['levelLearn'][0].lower(),
                data['formLearn'][0].lower(),
                data['grade'],
                data['stGroup']
            )
            Group.objects(name=group).update(set__name=group, upsert=True)
            document.group = Group.objects.get(name=group)


def load_user(_id):
    user = User.objects(pk=_id).first()
    return user


class Course(db.Document):
    archived = db.BooleanField(default=False)
    name = db.StringField()
    course_type = db.StringField(choices=["Технический", "Гуманитарный", "Программирование и т.п"])
    students = db.ListField(db.ReferenceField(User, reverse_delete_rule=PULL))
    description = db.StringField()
    lectures_auds = db.ListField(db.ReferenceField(Auditorium, reverse_delete_rule=PULL))
    # practice_auds = db.ListField(db.ReferenceField(Auditorium, reverse_delete_rule=PULL))
    # labs_auds = db.ListField(db.ReferenceField(Auditorium, reverse_delete_rule=PULL))
    teachers = db.ListField(db.ReferenceField(User, reverse_delete_rule=PULL))
    themes = db.ListField(db.EmbeddedDocumentField(Theme))
    links = db.ListField(db.ReferenceField('Course', reverse_delete_rule=PULL))

    def __unicode__(self):
        return self.name


class ProjectTeam(db.EmbeddedDocument):
    members = db.ListField(db.ReferenceField(User))
    empty_slots = db.IntField(min_value=0, max_value=8, default=8)
    is_full = db.BooleanField(default=False)

class Project(db.Document):
    name = db.StringField(required=True, max_length=255)
    link = db.StringField(required=True)
    disabled = db.BooleanField(required=True, default=False)
    disabledForJoin = db.BooleanField(default=False)
    teams = db.EmbeddedDocumentListField(ProjectTeam, max_length=3)


    def get_id(self):
        return self.pk

    def __unicode__(self):
        return self.name

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        for team in document.teams:
            team.empty_slots = 8 - len(team.members)
            if team.empty_slots == 0:
                team.is_full = True

        if len(p.teams) == 3 and all(team.is_full for team in document.teams):
            document.disabledForJoin = True

signals.post_save.connect(Project.post_save, sender=Project)
signals.post_save.connect(User.post_save, sender=User)