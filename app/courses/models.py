import mongoengine as db


class StudentUser(db.Document):
    fullname = db.StringField()
    group = db.StringField()

    def __unicode__(self):
        return self.fullname


class TeacherUser(db.Document):
    fullname = db.StringField()
    description = db.StringField()
    email = db.StringField()
    def __unicode__(self):
        return self.fullname


class Theme(db.EmbeddedDocument):
    name = db.StringField()
    description = db.StringField()
    start_date = db.StringField()
    end_date = db.StringField()

    def __unicode__(self):
        return self.name


class Coursetest(db.Document):
    name = db.StringField()
    description = db.StringField()
    groups = db.ListField(db.StringField())
    lectures_auds = db.ListField(db.StringField())
    practice_auds = db.ListField(db.StringField())
    labs_auds = db.ListField(db.StringField())
    teachers = db.ListField(db.ReferenceField(TeacherUser))
    themes = db.ListField(db.EmbeddedDocumentField(Theme))

    def __unicode__(self):
        return self.name

# first = TeacherUser(fullname='Иванов', description='Тест', email='asd@mail.ru')
# first.save()
# second = TeacherUser(fullname='Петров', description='Тест', email='asd@mail.ru')
# second.save()
# theme_first = Theme(name='Тестовая тема', description='Тестовое описание', start_date='21.12.2020', end_date='25.12.2020')
#
# theme_second = Theme(name='Тестовая тема 1', description='Тестовое описание 1', start_date='21.11.2020', end_date='25.11.2020')
#
# lectures_auds = ['Д-202', 'Д-205']
# groups = ['Ктбо1-2', 'Ктбо1-3']
# practice_auds = ['Д-202', 'Д-205']
# labs_auds = ['Д-202', 'Д-205']
# course = Coursetest(name='Тестовый курс',
#                     description='Описание курса',
#                     groups=groups,
#                     lectures_auds=lectures_auds,
#                     practice_auds=practice_auds,
#                     labs_auds=labs_auds,
#                     teachers=[first, second],
#                     themes=[theme_first, theme_second]
#                     )
# course.save()
# a = StudentUser(fullname='Иванов', group='Ктбо1-2')
# b = StudentUser(fullname='Петров', group='Ктсо1-2')
# a.save()
# b.save()
# for i in Coursetest.objects(groups = 'Ктбо1-2'):
#     print(i.id)
# a = Coursetest.objects()
# for j in a:
#     print(j.name)