from . import bp as auth
from mongoengine import DoesNotExist, MultipleObjectsReturned, CASCADE, DO_NOTHING
from flask_login import login_user, logout_user, login_required, current_user
from flask import (
    render_template,
    request,
    session,
    url_for,
    redirect,
    current_app
)
from app import oauth, login_manager
from app.models import User, OAuth2Token, Course


@auth.route('/login', methods=['GET'])
def index():
    return render_template(template_name_or_list='auth/login.html')


@auth.route('/oidc', methods=['GET', 'POST'])
def oidc():
    if session.get('oauth_token') is not None:
        return redirect(url_for('courses.index'))
    return oauth.azure.authorize_redirect(
        url_for('auth.authorized', _external=True)
    )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/oidc/authorized')
def authorized():
    token = oauth.azure.authorize_access_token()
    oidc_claims = oauth.azure.parse_id_token(token)

    oauth2token = OAuth2Token(name='azure', **token)
    try:
        user = User.objects.get(azure_oid=oidc_claims['oid'])
    except DoesNotExist:
        user = User(
            azure_oid=oidc_claims['oid']
        )
        resp = oauth.azure.get('me')
        resp.raise_for_status()
        profile_data = resp.json()

        user.email = profile_data['mail']
        user.fullname = profile_data['displayName']

        if current_app.config.get('ADMIN_EMAIL') == profile_data['mail']:
            user.role = 'Администратор'
        else:
            user.role = 'Студент'

        user.token = oauth2token
        user.save()

        login_user(user, remember=True)

        # TODO добавить константы, чтобы можно было использовать их вместо захардкоденной строки ("Студент"/"Преподователь")

        next_url = request.args.get('next')
        if next_url is None or not next_url.startswith('/'):
            if current_user.role == 'Администратор' or current_user.role == 'Преподаватель':
                next_url = url_for('course.index_view')
            else:
                next_url = url_for('courses.index')
        return redirect(next_url)
    except MultipleObjectsReturned:
        # TODO добавить какую-нибудь обработку
        # если это произошло, то мы в беде
        raise

    user.token = oauth2token
    user.save()
    login_user(user, remember=True)
    if current_user.role == 'Администратор' or current_user.role == 'Преподаватель':
        return redirect(url_for('course.index_view'))
    return redirect(url_for('courses.index'))


@auth.route('/display-info')
def display_info():
    resp = oauth.azure.get('me')
    return str(resp)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.oidc'))