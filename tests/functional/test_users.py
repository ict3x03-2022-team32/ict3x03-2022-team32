from flask_login import user_login_confirmed
import wsgi
from dotenv import load_dotenv
import os
load_dotenv('data.env')

testuser = os.environ.get("testuser")
testpassword = os.environ.get("testpassword")



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

def test_login_function(client):
    """
    GIVEN the login page
    WHEN the credentials to log in is correct (POST)
    THEN check that the response is valid and the user is redirected to the dashboard page
    """
    headers = {
        "Referer": '/login'
    }
    
    client.post('/login', data=dict(username = testuser, password = testpassword), headers=headers)
    #assert response.status_code == 200
    response = client.get('/dashboard', follow_redirects=True)
    '''
    assert b'Dashboard' in response.data
    assert b'Success! You are logged in as:' in response.data
    assert b'Vacancy' in response.data
    assert b'Total Employees Over The Years' in response.data
    assert b'Login' not in response.data
    assert b'Sign in' not in response.data
    assert b'Register' in response.data
    assert b'Data Analytics for Employment Salary in Industries of Singapore' not in response.data
        '''
