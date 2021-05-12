import mongoengine as db
from flask_login import UserMixin
from flask import url_for
from jinja2 import Markup
from flask_admin.form import DatePickerWidget
from flask_admin.form.widgets import DatePickerWidget
from mongoengine import CASCADE, PULL


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


def load_user(_id):
    user = User.objects(pk=_id).first()
    return user


class Course(db.Document):
    archived = db.BooleanField()
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
