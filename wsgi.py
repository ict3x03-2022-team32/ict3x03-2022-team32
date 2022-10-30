
from application import app

#for site wide CSRF Protection
from flask_wtf.csrf import CSRFProtect, CSRFError
csrf = CSRFProtect(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if __name__=="__main__":
    app.run()
