from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from urllib.parse import quote


app = Flask(__name__)
app.config['SECRET_KEY'] = "JLKJJJO3IURYoiouolnojojouuoo=5y9y9youjuy952oohhbafdnoglhoho"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenseDB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://root:%s@localhost:3306/expenseDB' % quote('P@ssw0rd123'))
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from application import routes