from flask import Flask
from werkzeug.security import generate_password_hash

from blog.article.views import article
from blog.auth.views import auth
from blog.index.views import index
from blog.user.views import user_app
from .api import init_api
from .author.views import author
from blog.extension import login_manager, migrate, csrf, admin
from blog.models import Tag, User
from blog.models.database import db


VIEWS = [
    user_app,
    article,
    index,
    auth,
    author,
]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.configs')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

    register_extensions(app)
    register_blueprint(app)
    register_api(app)
    return app


def register_api(app: Flask):
    api = init_api(app)


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

        if Tag.query.count() == 0:
            create_tags()

        if User.query.count() == 0:
            create_users()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprint(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)

    from blog import admin
    admin.register_views()


def create_tags():
    tags = ("flask", "django", "python", "sqlalchemy", "news")
    for name in tags:
        tag = Tag(name=name)
        db.session.add(tag)

    db.session.commit()


def create_users():
    db.session.add(
        User(email="name@email.com", password=generate_password_hash("test"))
    )
    db.session.commit()
