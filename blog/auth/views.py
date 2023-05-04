from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import check_password_hash

from sqlalchemy.exc import IntegrityError

from blog.forms.user import UserRegisterForm, UserloginForm
from blog.models.user import User, db

auth = Blueprint("auth", __name__, url_prefix="/auth", static_folder="../static")


@auth.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    error = None
    form = UserRegisterForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect("/")

    return render_template("auth/register.html", form=form, error=error)


@auth.route('login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    error = None
    form = UserloginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            form.email.errors.append("Check your login details")
            return render_template("auth/login.html", form=form)

        login_user(user)
        return redirect("/")

    return render_template("auth/login.html", form=form, error=error)


# @auth.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         return render_template(
#             "auth/login.html"
#         )
#     from blog.models.user import User
#
#     email = request.form.get("email")
#     password = request.form.get("password")
#     user = User.query.filter_by(email=email).first()
#
#     if not user or not check_password_hash(user.password, password):
#         flash("Check your login details")
#         return redirect(url_for(".login"))
#     login_user(user)
#     return redirect(url_for("user.profile", pk=user.id))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
