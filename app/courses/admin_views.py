from flask_admin.contrib.mongoengine import ModelView, EmbeddedForm
from .models import *
from bson import ObjectId


class TeacherView(ModelView):
    column_list = ['fullname', 'description', 'email']
    column_labels = {
        'fullname': 'ФИО',
        'description': 'Описание',
        'email': 'Электронная почта'
    }
    form_args = {
        'fullname': {
            'label': 'ФИО',
        },
        'description': {
            'label': 'Описание',
        },
        'email': {
            'label': 'Почта',
        }
    }


class StudentView(ModelView):
    column_list = ['fullname', 'group', 'courses']
    column_labels = {
        'fullname': 'ФИО',
        'group': 'Группа',
        'courses': 'Курсы'
    }
    form_args = {
        'fullname': {
            'label': 'ФИО',
        },
        'group': {
            'label': 'Группа',
        },
        'courses': {
            'label': 'Курсы',
        }
    }


# class ThemeEmbed(EmbeddedForm):
#     form_columns = ('name', 'description', 'start_date', 'end_date')
    # form_labels = {
    #     'name': 'Название',
    #     'description': 'Описание',
    #     'start_date': 'Начало',
    #     'end_date': 'Конец'
    # }
    # form_args  = {
    #     'name': {
    #         'label': 'Название'
    #     },
    #     'description': {
    #         'label': 'Описание'
    #     },
    #     'start_date': {
    #         'label': 'Начало'
    #     },
    #     'end_date': {
    #         'label': 'Конец'
    #     }
    # }



class CourseView(ModelView):
    column_list = ['name', 'description', 'lectures_auds', 'practice_auds', 'labs_auds', 'teachers', 'themes']
    column_labels = {
        'name': 'Название',
        'description': 'Описание',
        'lectures_auds': 'Аудитории для лекций',
        'practice_auds': 'Аудитории для практических работ',
        'labs_auds': 'Аудитории для лабораторных работ',
        'teachers': 'Преподаватели',
        'themes': 'Темы'
    }
    form_args = {
        'name': {
            'label': 'Название'
        },
        'description': {
            'label': 'Описание'
        },
        'lectures_auds': {
            'label': 'Aудитории для лекций'
        },
        'practice_auds': {
            'label': 'Aудитории для практический занятий'
        },
        'labs_auds': {
            'label': 'Aудитории для лабораторных занятий'
        },
        'teachers': {
            'label': 'Преподаватели'
        },
        'themes': {
            'label': 'Темы'
        },

    }

    form_subdocuments = {
        'themes': {
            'form_subdocuments': {
                None: {
                    'form_columns': ('name', 'description', 'start_date', 'end_date'),
                    'form_args': {
                        'name': {
                            'label': 'Название'
                        },
                        'description': {
                            'label': 'Описание'
                        },
                        'start_date': {
                            'label': 'Начало'
                        },
                        'end_date': {
                            'label': 'Конец'
                        }
                    }
                }
            }
        }
    }

    # def get_query(self):
    #     courses = Course.objects(teachers=ObjectId('604e5dd6aef5a6bbe35f6d1c'))
    #     return courses
    #
    # def get_count_query(self):
    #     return self.get_query().count()


class GroupView(ModelView):
    column_list = ['name']
    column_labels = {
        'name': 'Название'
    }
    form_args = {
        'name': {
            'label': 'Название',
        },

    }


class AuditoriumView(GroupView):
    pass



