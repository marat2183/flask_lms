from flask_admin.contrib.mongoengine import ModelView, EmbeddedForm
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import url_for, redirect, request, render_template
from flask_admin.contrib.mongoengine.ajax import QueryAjaxModelLoader, DEFAULT_PAGE_SIZE
from wtforms.widgets import TextArea
from wtforms import TextAreaField

from app.models import User, Course
from bson import ObjectId
from flask_admin.form import rules


class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditorWidget()


class FilteredByRoleAjaxModelLoader(QueryAjaxModelLoader):
    def get_list(self, term, offset=0, limit=DEFAULT_PAGE_SIZE):
        role = self.filter_by_role
        if term:
            return (
                self.model.objects(role=role, fullname____icontains=term)
            )
        else:
            return (
                self.model.objects(role=role)
            )

    def __init__(self, name, model, **options):
        super(FilteredByRoleAjaxModelLoader, self).__init__(name, model, **options)
        self.filter_by_role = options.get('filter_by_role')


class MyModelAdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == 'Администратор':
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated and current_user.role == 'Преподаватель':
            return redirect(url_for('course.index_view'))
        elif current_user.is_authenticated and current_user.role == 'Студент':
            return redirect(url_for('courses.index'))
        else:
            return redirect(url_for('auth.index'))


class MyModelTeacherView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == 'Преподаватель':
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('courses.index'))
        return redirect(url_for('auth.index'))


class MyModelAdminTeacherView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and (
                current_user.role == 'Администратор' or current_user.role == 'Преподаватель'):
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('courses.index'))
        return redirect(url_for('auth.index'))

    @property
    def can_create(self):
        return current_user.role == 'Администратор'

    @property
    def can_edit(self):
        return current_user.role == 'Администратор' or current_user.role == 'Преподаватель'

    @property
    def can_delete(self):
        return current_user.role == 'Администратор'


class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        if current_user.is_authenticated and (current_user.role == 'Администратор' or current_user.role == 'Преподаватель'):
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('courses.index'))
        return redirect(url_for('auth.index'))

    @expose('/')
    def index(self):
        return self.render(template='admin/master-extended.html')


class TeacherView(MyModelAdminView):
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


class StudentView(MyModelAdminView):
    def search_placeholder(self):
        return 'Введите ФИО'

    form_excluded_columns = ['azure_oid', 'token', 'active']
    column_list = ['fullname', 'role']
    page_size = 25
    column_searchable_list = ['fullname']
    column_labels = {
        'fullname': 'ФИО',
        'group': 'Группа',
        'role': 'Роль'
    }
    form_args = {
        'fullname': {
            'label': 'ФИО',
            'render_kw': {
                'placeholder': 'Введите ФИО',
            },
        },
        'email': {
            'label': 'Электронная почта',
            'render_kw': {
                'placeholder': 'Введите электронную почту',
            },
        },
        'group': {
            'label': 'Группа',

        },
        'role': {
            'label': 'Роль',
            'render_kw': {
                'placeholder': 'Выберите роль',
            },
        },
        'description': {
            'label': 'Описание',
             'render_kw': {
                  'placeholder': 'Введите описание',
            },
        },
    }


class CourseView(MyModelAdminTeacherView):
    # form_overrides = dict(description=CKEditorField)
    create_template = '/admin/new_edit.html'
    edit_template = '/admin/new_edit.html'
    column_list = ['name', 'description', 'lectures_auds', 'teachers', 'themes']
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
            'label': 'Название',
            'render_kw': {
                'placeholder': 'Введите название курса'
            }
        },
        'description': {
            'label': 'Описание',
            'render_kw': {
                'placeholder': 'Введите описание курса'
            }
        },
        'lectures_auds': {
            'label': 'Aудитории для лекций'
        },
        # 'practice_auds': {
        #     'label': 'Aудитории для практический занятий'
        # },
        # 'labs_auds': {
        #     'label': 'Aудитории для лабораторных занятий'
        # },
        'teachers': {
            'label': 'Преподаватели'
        },
        'themes': {
            'label': 'Темы'
        },
        'students': {
            'label': 'Участники'
        },
        'links': {
            'label': 'Пересечения'
        },
        'course_type': {
            'label': 'Тип'
        },

    }

    form_ajax_refs = {
        'teachers': FilteredByRoleAjaxModelLoader
            (
                name='teachers',
                model=User,
                fields=['fullname', 'role', 'id'],
                filter_by_role='Преподаватель',
                minimum_input_length=0,
                placeholder='Пожалуйста, выберите преподавателей',
            ),
        'students': FilteredByRoleAjaxModelLoader
            (
                name='students',
                model=User,
                fields=['fullname', 'role', 'id'],
                filter_by_role='Студент',
                minimum_input_length=0,
                placeholder='Пожалуйста, выберите студентов'
            ),
        # 'labs_auds': {
        #         'fields': ('name',),
        #         'placeholder': 'Пожалуйста, выберите аудитории',
        #         'minimum_input_length': 0,
        # },

        'lectures_auds': {
            'fields': ('name',),
            'placeholder': 'Пожалуйста, выберите аудитории',
            'minimum_input_length': 0,
        },
        # 'practice_auds': {
        #     'fields': ('name',),
        #     'placeholder': 'Пожалуйста, выберите аудитории',
        #     'minimum_input_length': 0,
        # },

    }
    form_subdocuments = {
        'themes': {
            'form_subdocuments': {
                None: {
                    'form_overrides': dict(description=CKEditorField),
                    'form_columns': ('name', 'description'),
                    'form_args': {
                        'name': {
                            'label': 'Название'
                        },
                        'description': {
                            'label': 'Описание'
                        },
                        # 'start_date': {
                        #     'label': 'Начало',
                        #     'format': '%d.%m.%Y',
                        # },
                        # 'end_date': {
                        #     'label': 'Конец',
                        #     'format': '%d.%m.%Y',
                        # }
                    },
                    # 'form_widget_args':{
                    #     'start_date': {
                    #         'data-date-format': u'DD.MM.YYYY',
                    #         'data-show-meridian': 'True'
                    #     },
                    #     'end_date': {
                    #         'data-date-format': u'DD.MM.YYYY',
                    #         'data-show-meridian': 'True'
                    #     }
                    # }
                }
            }
        }
    }

    def get_query(self):
        if current_user.role == "Преподаватель":
            courses = Course.objects(teachers=ObjectId(current_user.id))
        else:
            courses = Course.objects()
        return courses

    def get_count_query(self):
        return self.get_query().count()


class GroupView(MyModelAdminView):
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



