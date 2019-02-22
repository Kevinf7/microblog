import os

class Config(object):
    #Flask settings
    #SECRET_KEY = os.urandom(24)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'
    DEBUG=True

    #Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    POSTS_PER_PAGE = 5

    #CKEditor settings
    CKEDITOR_HEIGHT=200
    CKEDITOR_WIDTH=800
    CKEDITOR_PKG_TYPE='basic'
