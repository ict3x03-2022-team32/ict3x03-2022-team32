from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from urllib.parse import quote


app = Flask(__name__)
app.config['SECRET_KEY'] = "JLKJJJO3IURYoiouolnojojouuoo=5y9y9youjuy952oohhbafdnoglhoho"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenseDB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://root:%s@localhost:3306/expenseDB' % quote('P@ssw0rdpsBenU7Wka'))
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

#for site wide CSRF Protection
from flask_wtf.csrf import CSRFProtect, CSRFError
csrf = CSRFProtect(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(app, key_func=get_remote_address)


from application import routes
