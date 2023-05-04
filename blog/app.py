from flask import Flask

from blog.article.views import article
from blog.auth.views import auth
from blog.index.views import index
from blog.user.views import user_app
from blog.extension import login_manager, migrate, csrf
from blog.models.user import User
from blog.models.database import db


VIEWS = [
    user_app,
    article,
    index,
    auth,
]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.configs')

    csrf.init_app(app)

    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprint(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)
