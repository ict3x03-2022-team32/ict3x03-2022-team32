
from application import app

#for site wide CSRF Protection
from flask_wtf.csrf import CSRFProtect, CSRFError
csrf = CSRFProtect(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(app, key_func=get_remote_address)

if __name__=="__main__":
    app.run()
