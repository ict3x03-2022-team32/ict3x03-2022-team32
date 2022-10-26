
from application import app

#for site wide CSRF Protection
from flask_wtf.csrf import CSRFProtect, CSRFError
csrf = CSRFProtect(app)

if __name__=="__main__":
    app.run()
