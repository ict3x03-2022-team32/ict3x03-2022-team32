from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from urllib.parse import quote
from dotenv import load_dotenv
import logging
from flask_web_log import Log
import os
import csv
load_dotenv('data.env')

db_key = os.environ.get("db_key")
db_username = os.environ.get("db_username")
db_pwd = os.environ.get("db_pwd")
email = os.environ.get("mail_email")
pwd = os.environ.get("mail_pwd")

app = Flask(__name__)

logging.basicConfig(filename = 'web.log', level=logging.DEBUG, 
format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config["LOG_TYPE"] = "CSV"
Log(app)
app.config['SECRET_KEY'] = db_key
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenseDB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = (db_username % quote(db_pwd))
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = pwd
app.config['MAIL_DEFAULT_SENDER'] = email
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from application import routes
