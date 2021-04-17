from . import bp as courses_bp
from flask import render_template, request, session
from flask_login import login_required, current_user
from .services import *


@courses_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        return render_template(template_name_or_list='courses/courses.html')
    else:
        course_id = request.args.get('id')
        if course_id:
            course = get_courses_by_id(course_id)
            return render_template(template_name_or_list='courses/course_page.html', course=course)
        else:
            courses = get_courses_able_to_join(current_user.id)
            return render_template(template_name_or_list='courses/courses.html', courses = courses)
        return render_template(template_name_or_list='courses/courses.html')

@courses_bp.route('/active', methods=['GET', 'POST'])
@login_required
def user_courses():
    if request.method == "POST":
        return render_template(template_name_or_list='courses/courses.html')
    else:
        courses = get_user_courses(current_user.id)
        return render_template(template_name_or_list='courses/courses.html', courses=courses)