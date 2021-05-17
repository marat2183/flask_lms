from . import bp as courses_bp
from flask import render_template, request, session, jsonify, url_for, abort
from flask_login import login_required, current_user
from .services import *


@courses_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    icons = {
        'Технический': url_for('static', filename='img/courses/lessons/icons/tech.svg'),
        'Гуманитарный': url_for('static', filename='img/courses/lessons/icons/marketing.svg'),
        'Программирование и т.п': url_for('static', filename='img/courses/lessons/icons/marketing.svg')
    }
    if request.method == "POST":
        return ''
    else:
        course_id = request.args.get('id')
        if course_id:
            course = get_courses_by_id(course_id)
            if course is None:
                return abort(404)
            return render_template(template_name_or_list='courses/course_page.html', course=course, icons=icons)
        else:
            courses = get_courses_able_to_join(current_user.id)
            return render_template(template_name_or_list='courses/courses.html', courses = courses, icons=icons)


@courses_bp.route('/active', methods=['GET', 'POST'])
@login_required
def user_courses():
    icons = {
        'Технический': url_for('static', filename='img/courses/lessons/icons/tech.svg'),
        'Гуманитарный': url_for('static', filename='img/courses/lessons/icons/marketing.svg'),
        'Программирование и т.п': url_for('static', filename='img/courses/lessons/icons/marketing.svg')
    }
    if request.method == "POST":
        return ''
    else:
        courses = get_user_courses(current_user.id)
        return render_template(template_name_or_list='courses/active_courses.html', courses=courses, icons=icons)


@courses_bp.route('/add_to_course', methods=['GET', 'POST'])
@login_required
def add_to_course():
    course_id = request.form.get('course_id')
    status = join_to_course(current_user.id, course_id)
    if status:
        data = {'status': 'success'}
        return jsonify(data)
    else:
        data = {'status': 'error'}
        return jsonify(data)
