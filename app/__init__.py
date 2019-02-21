from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
#Which page to redirect to page if user is not logged in
login.login_view = 'login'

migrate = Migrate(app,db)
bootstrap = Bootstrap(app)
moment = Moment(app)
ckeditor = CKEditor(app)

#setup log files
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    #Log size rotates at 10KB so file size doesn't grow too big
    #Keeps the last 10 log files as backup
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    #Provide custom formatting for log messages
    file_handler.setFormatter(logging.Formatter( \
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]' \
    ))
    #set logging level to INFO in file logger
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    #set logging level to INFO in application logger
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import models, views, errors
