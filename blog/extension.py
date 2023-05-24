from flask_admin import Admin
# from flask_combo_jsonapi import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from combojsonapi.spec import ApiSpecPlugin


def create_api_spec_plugin(app):
    api_spec_plugin = ApiSpecPlugin(
        app=app,
        tags={
            'Tag': 'Tag API',
            'Article': 'Articles API',
            'Author': 'Author API',
            'User': 'Users API',
        }
    )

    return api_spec_plugin


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
admin = Admin(name='blog admin panel', template_mode='bootstrap4')
# api = Api()
