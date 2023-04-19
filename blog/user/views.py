from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

user = Blueprint('user', __name__, static_folder='../static', url_prefix='/users')

USERS = {
    1: 'User1',
    2: 'User2',
    3: 'User3',
}


@user.route('/')
def user_list():
    return render_template(
        'users/list.html',
        users=USERS,
    )


@user.route('/<int:pk>')
def get_users(pk: int):
    try:
        user_name = USERS[pk]
    except KeyError:
        raise NotFound(f'User id {pk} not found')

    return render_template(
        'users/detail.html',
        user_name=user_name,
    )
