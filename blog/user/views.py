from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound


user_app = Blueprint('user', __name__, static_folder='../static', url_prefix='/users')


@user_app.route('/')
def user_list():
    from blog.models.user import User
    users = User.query.all()
    return render_template(
        "users/list.html",
        users=users
    )


@user_app.route('/<int:pk>')
@login_required
def profile(pk: int):
    from blog.models.user import User
    _user = User.query.filter_by(id=pk).one_or_none()
    if _user is None:
        raise NotFound(f"User id:{pk}, not found")
    return render_template(
        "users/detail.html",
        user=_user
    )
