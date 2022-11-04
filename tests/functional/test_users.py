from flask_login import user_login_confirmed
from dotenv import load_dotenv
import os
import random
import sys
import fileinput
import pytest
import time 

#selenium libraries
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#recaptcha libraries
import speech_recognition as sr
#import ffmpy
import requests
import urllib
import pydub


load_dotenv('data.env')

testuser = os.environ.get("testuser")
testpassword = os.environ.get("testpassword")
pub_key = os.environ.get("pub_key")
secret = os.environ.get("private_key")
testregisteruser = os.environ.get("testregisteruser")






##################################################################################################################################################################################    
def delay():
    time.sleep(random.randint(2,3))

"""
def test_index_page():
    
    #GIVEN the index page
    #WHEN the '/' page is requested (GET)
    #THEN check that the response is valid
    
    driver = webdriver.Chrome(executable_path="C:\\Users\\RH\\Desktop\\chromedriver_win32\\chromedriver.exe")
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("http://localhost:5000/")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #yield
    delay()
    driver.quit()
"""
'''
def test_register_page_username():
    driver = webdriver.Chrome(executable_path="C:\\Users\\RH\\Desktop\\chromedriver_win32\\chromedriver.exe")
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("http://localhost:5000/register")

    delay()

    frames = driver.find_element(By.XPATH,"/html/body/div[2]/div[4]")
    #frames2 = frames.find_elements(By.TAG_NAME,"iframe")

    user_name=driver.find_element(By.ID, "username")
    user_name.send_keys('<SCRIPT SRC=//xss.rock/.j>')

    invalidXPATH = '/html/body/div[1]/div[2]/div[2]/div/div/div/div/form/div[2]/div/span'

    driver.find_element(By.ID, "submit").click()
    checkifmessageexist = driver.find_element(By.XPATH, invalidXPATH)
    assert checkifmessageexist == '[Invalid input.]'
'''
    
def recaptcha(driver):
    #switch to recaptcha frame
    #frames = driver.find_elements_by_tag_name("iframe")
    frames = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(frames)
    #driver.switch_to.frame(frames[0])
    delay()
    

    #click on checkbox to activate recaptcha
    driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()


    # switch to recaptcha audio control frame
    delay()
    driver.switch_to.default_content()
    #frames = driver.find_elements_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
    try:
        frames = driver.find_element(By.XPATH,"/html/body/div[2]/div[4]")
        s=frames.text
    except NoSuchElementException:
        return True
    frames2 = frames.find_elements(By.TAG_NAME,"iframe")
    driver.switch_to.frame(frames2[0])
    delay()

    #Click on audio challenge
    driver.find_element(By.ID,"recaptcha-audio-button").click()

    #switch to recaptcha audio challenge frame
    delay()
    driver.switch_to.default_content()
    frames=driver.find_element(By.TAG_NAME,"iframe")
    #driver.switch_to.frame(frames[-1])
    driver.switch_to.frame(frames)
    

    #click on play button
    delay()
    driver.find_elements(By.XPATH,"/html/body/div/div/div[3]/div/button").click()

    #Get the mp3 audio file
    delay()
    src = driver.find_element(By.ID,"audio-source").get_attribute("src")
    print(f"[INFO] Audio src: {src}")
    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    #download the mp3 audio file from the source
    urllib.request.urlretrieve(src, path_to_mp3)

    #load downloaded mp3 audio file as .wav
    sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    sound.export(path_to_wav, format="wav")
    sample_audio = sr.AudioFile(sr.AudioFile(path_to_wav))
    delay()

    # translate audio to text with google voice recognition
    r = sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)

    key=r.recognize_google(audio)
    print("[INFO] Recaptcha Passcode: %s" %key)

    #key in results and submit
    driver.find_element(By.ID,"audio-response").send_keys(key.lower())
    driver.find_element(By.ID,'audio-response').send_keys(Keys.ENTER)

    time.sleep(5)
    driver.switch_to.default_content()
    time.sleep(5)
    driver.find_element(By.ID, "recaptcha-demo-submit").click()
    return True






def test_login_page():
    """
    GIVEN the index page
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    #chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')
    #driver = webdriver.Chrome(executable_path="C:\\Users\\RH\\Desktop\\chromedriver_win32\\chromedriver.exe")
    #driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome(options=chrome_options, executable_path="C:\\Users\\RH\\Desktop\\chromedriver_win32\\chromedriver.exe")
    driver=uc.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("http://localhost:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title
    delay()

    recaptcha(driver)
    

    #yield
    delay()
    driver.quit()






'''


def test_index_page(client):
    """
    GIVEN the index page
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    #global driver
    driver = webdriver.Chrome(executable_path="C:\\Users\\RH\\Desktop\\chromedriver_win32\\chromedriver.exe")
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("http://localhost:5000/")
    #flask_app = app('conftest.cfg')
    response = client.get('/')
    assert response.status_code == 200
    assert b'Data Analytics for Employment Salary in Industries of Singapore' in response.data
    assert b'Register' in response.data
    assert b'Login' in response.data
    assert b'Home' in response.data
    assert b'dadwad' not in response.data
    #yield
    time.sleep(10)
    driver.quit()
'''
'''
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
