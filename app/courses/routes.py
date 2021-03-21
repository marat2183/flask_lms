from courses import bp as courses_bp
from flask import render_template, request
from flask_login import login_required
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
        return render_template(template_name_or_list='courses/courses.html')

