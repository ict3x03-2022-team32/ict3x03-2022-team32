'''
import pytest
import wsgi
from dotenv import load_dotenv
import os
from urllib.parse import quote
from flask import Flask


load_dotenv('data.env')

#####################################################################################################################
# First some imports. I'm assuming you're using Flask-WTF for CSRF protection.
import flask
from flask import Flask
from flask.testing import FlaskClient as BaseFlaskClient
from flask_wtf.csrf import generate_csrf

# Flask's assumptions about an incoming request don't quite match up with
# what the test client provides in terms of manipulating cookies, and the
# CSRF system depends on cookies working correctly. This little class is a
# fake request that forwards along requests to the test client for setting
# cookies.

class RequestShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    """
    def __init__(self, client):
        self.client = client
        self.vary = set({})

    def set_cookie(self, key, value='', *args, **kwargs):
        "Set the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.set_cookie(
            server_name, key=key, value=value, *args, **kwargs
        )

    def delete_cookie(self, key, *args, **kwargs):
        "Delete the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.delete_cookie(
            server_name, key=key, *args, **kwargs
        )

# We're going to extend Flask's built-in test client class, so that it knows
# how to look up CSRF tokens for you!
class FlaskClient(BaseFlaskClient):
    @property
    def csrf_token(self):
        # First, we'll wrap our request shim around the test client, so that
        # it will work correctly when Flask asks it to set a cookie.
        request = RequestShim(self) 
        # Next, we need to look up any cookies that might already exist on
        # this test client, such as the secure cookie that powers `flask.session`,
        # and make a test request context that has those cookies in it.
        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)
        with flask.current_app.test_request_context(
                "/login", environ_overrides=environ_overrides,
            ):
            # Now, we call Flask-WTF's method of generating a CSRF token...
            csrf_token = generate_csrf()
            # ...which also sets a value in `flask.session`, so we need to
            # ask Flask to save that value to the cookie jar in the test
            # client. This is where we actually use that request shim we made! 
            flask.current_app.session_interface.save_session(flask.current_app, flask.session, request)
            # And finally, return that CSRF token we got from Flask-WTF.
            return csrf_token

    # Feel free to define other methods on this test client. You can even
    # use the `csrf_token` property we just defined, like we're doing here!
    def login(self, email, password):
        return self.post("/login", data={
            "email": email,
            "password": password,
            "csrf_token": self.csrf_token,
        }, follow_redirects=True)

    def logout(self):
        return self.get("/logout", follow_redirects=True)


#####################################################################################################################

@pytest.fixture
def app():
    app = wsgi.app
    app.test_client_class = FlaskClient
    app.config['TESTING'] = True
    app.config['WTF_CSRF_METHODS'] = []
    
    # other setup can go here
    yield app
    

    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


'''