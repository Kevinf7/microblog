import os

class Config(object):
    #Flask settings
    #SECRET_KEY = os.urandom(24)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'
    DEBUG=True

    #Flask-SQLAlchemy settings
    #SQLALCHEMY_DATABASE_URI='mysql+pymysql://u517628157_kf:kSdxKhRTm1Nf@sql171.main-hosting.eu/u517628157_tt'
    #SQLALCHEMY_DATABASE_URI='mysql+pymysql://kevinf7:Sydn3y3030@kevinf7.mysql.pythonanywhere-services.com/kevinf7$top_trumps'
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://kevin:Sydn3y30@localhost:3306/blog'
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    POSTS_PER_PAGE = 5

    #CKEditor settings
    CKEDITOR_HEIGHT=200
    CKEDITOR_WIDTH=800
    CKEDITOR_PKG_TYPE='standard'
