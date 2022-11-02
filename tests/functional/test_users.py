from flask_login import user_login_confirmed
import wsgi
from dotenv import load_dotenv
import os
import sys
import fileinput


load_dotenv('data.env')

testuser = os.environ.get("testuser")
testpassword = os.environ.get("testpassword")
pub_key = os.environ.get("pub_key")
secret = os.environ.get("private_key")
testregisteruser = os.environ.get("testregisteruser")





##################################################################################################################################################################################

def test_index_page(client):
    """
    GIVEN the index page
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    #flask_app = app('conftest.cfg')
    response = client.get('/')
    assert response.status_code == 200
    assert b'Data Analytics for Employment Salary in Industries of Singapore' in response.data
    assert b'Register' in response.data
    assert b'Login' in response.data
    assert b'Home' in response.data
    assert b'dadwad' not in response.data

def test_login_page(client):
    """
    GIVEN the login page
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/login')
    assert response.status_code == 200
    assert b'User Name' in response.data
    assert b'Password' in response.data
    assert b'Sign in' in response.data
    assert b'Register' in response.data
    assert b'Login' in response.data
    assert b'Home' in response.data
    assert b'Data Analytics for Employment Salary in Industries of Singapore' not in response.data

def test_index_page__not_logged_in(client):
    """
    GIVEN the login page
    WHEN the '/dashboard' page is requested (GET) as an unauthenticated user
    THEN check that the user will be redirected to log in page
    """
    response = client.get('/dashboard')
    assert response.status_code == 302

# To hook up this extended test client class to your Flask application,
# assign it to the `test_client_class` property, like this:
#app = Flask(__name__)
#app.test_client_class = FlaskClient

# Now in your tests, you can request a test client the same way
# that you normally do:
#client = app.test_client()
#client.login(testuser, testpassword)

def test_login_function(client):
    
    with client:
        
        #GIVEN the login page
        #WHEN the credentials to log in is correct (POST)
        response = client.post('/login', data={"csrf_token":client.csrf_token, "username":testuser, "password":testpassword, "g-recaptcha-response":"", "submit":"Sign+in"}, follow_redirects=True)
        
        #THEN check that the response is valid and the user is redirected to the dashboard page
        assert b'Dashboard' in response.data
        assert b'Success! You are logged in as:' in response.data
        assert b'Vacancy' in response.data
        assert b'Total Employees Over The Years' in response.data
        assert b'Login' not in response.data
        assert b'Sign in' not in response.data
        assert b'Register' not in response.data
        assert b'Data Analytics for Employment Salary in Industries of Singapore' not in response.data

def test_register_function(client):

    temp = testregisteruser
    temp = temp[:-1] + str(int(temp[-1])+1)

    # This for loop scans and searches each line in the file
    # By using the input() method of fileinput module
    for line in fileinput.input("data.env", inplace=True):
    
        # This will replace string "testregisteruser" + x  with "testregisteruser"+ x+1 in each line
        line = line.replace(testregisteruser, temp)
        
        # write() method of sys module redirects the .stdout is redirected to the file
        sys.stdout.write(line)
    
    with client:

        #GIVEN the Register page
        #WHEN the user information input to create account is valid (POST)
        response = client.post('/register', data={"csrf_token":client.csrf_token, "username":testregisteruser, "email_address":temp +"@temp.com", "password1":testpassword, "password2":testpassword, "g-recaptcha-response":"", "submit":"Create+Account"}, follow_redirects=True)

        #THEN check that the response is valid and the new user account is created and is redirected to the dashboard page
        assert b'Dashboard' in response.data
        assert b'Account created successfully! You are now logged in as' in response.data
        assert b'Vacancy' in response.data
        assert b'Total Employees Over The Years' in response.data
        assert b'Login' not in response.data
        assert b'Sign in' not in response.data
        assert b'Register' not in response.data
        assert b'Data Analytics for Employment Salary in Industries of Singapore' not in response.data

'''
def test_forgetPassword_function(client):
    
    with client:

        #GIVEN the Register page
        #WHEN the user information input to create account is valid (POST)
        response = client.post('/register', data={"csrf_token":client.csrf_token, "username":testregisteruser, "email_address":temp +"@temp.com", "password1":testpassword, "password2":testpassword, "g-recaptcha-response":"", "submit":"Create+Account"}, follow_redirects=True)

        #THEN check that the response is valid and the new user account is created and is redirected to the dashboard page
        assert b'Dashboard' in response.data
        assert b'Account created successfully! You are now logged in as' in response.data
        assert b'Vacancy' in response.data
        assert b'Total Employees Over The Years' in response.data
        assert b'Login' not in response.data
        assert b'Sign in' not in response.data
        assert b'Register' not in response.data
        assert b'Data Analytics for Employment Salary in Industries of Singapore' not in response.data
'''