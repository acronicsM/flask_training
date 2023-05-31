import os
from dotenv import load_dotenv


load_dotenv()

DEBUG = os.getenv('FLASK_DEBUG', default=True)

SECRET_KEY = os.getenv('SECRET_KEY', default='nv+b(%k6bn(j(=_w%30nnxb!85nb07b4-#t6(3_)@zr=)-c@&8')

SQLALCHEMY_TRACK_MODIFICATION = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default='sqlite:///db.sqlite')

WTF_CSRF_ENABLED = True

FLASK_ADMIN_SWATCH = 'pulse'

OPENAPI_URL_PREFIX = '/api/docs/'
OPENAPI_SWAGGER_UI_PATH = '/'
OPENAPI_SWAGGER_UI_VERSION = '3.22.0'
