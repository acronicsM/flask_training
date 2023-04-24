from os import getenv, path

from flask import Flask

from json import load as js_load

from blog.article.views import article
from blog.auth.views import auth
from blog.index.views import index
from blog.user.views import user

from blog.extension import db, login_manager
from blog.models import User


CONFIG_PATH = getenv("CONFIG_PATH", path.join("../dev_config.json"))

VIEWS = [
    user,
    article,
    index,
    auth,
]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_file(CONFIG_PATH, load=js_load)
    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app):
    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprint(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)
