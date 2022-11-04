from dotenv import load_dotenv
import os
import random
import time 

#selenium libraries
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

load_dotenv('data.env')

testuser = os.environ.get("testuser")
testpassword = os.environ.get("testpassword")
pub_key = os.environ.get("pub_key")
secret = os.environ.get("private_key")
testregisteruser = os.environ.get("testregisteruser")



##################################################################################################################################################################################    
def delay():
    time.sleep(random.randint(2,3))


def test_login_page_WrongUsernameField():
    """
    #GIVEN the login page
    #WHEN the '/login' page is requested (POST) with a invalid username and a valid password is send
    #THEN check that the response is valid and the user is prompt an error message and not logged in
    """

    option = webdriver.ChromeOptions()
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    
    #driver=uc.Chrome(headless=True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    driver.maximize_window()
    #driver.get("http://localhost:5000/login")
    driver.get("http://securitycrusaders:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    #Input a malicious "User Name"
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys("<script/src=//Ǌ.₨></script>")

    #Input a valid Password
    password = driver.find_element(By.ID,"password")
    password.send_keys(testpassword)
    delay()

    #Click Sign in button
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user received an error message
    fail = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']").get_attribute("textContent")
    assert fail[33:86] == "Username and password are not match! Please try again"
    delay()

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except:
        not_found = True

    assert not_found

    #yield
    delay()
    driver.quit()

def test_login_page_WrongPasswordField():
    """
    #GIVEN the login page
    #WHEN the '/login' page is requested (POST) with a correct username and a wrong password is send
    #THEN check that the response is valid and the user is prompt an error message and not logged in
    """

    option = webdriver.ChromeOptions()
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    
    #driver=uc.Chrome(headless=True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    driver.maximize_window()
    #driver.get("http://localhost:5000/login")
    driver.get("http://securitycrusaders:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    #Input a valid User Name
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys(testuser)

    #Input a invalid Password
    password = driver.find_element(By.ID,"password")
    password.send_keys('testingincorrectpassword')
    delay()

    #Click Sign in button
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user received an error message
    fail = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']").get_attribute("textContent")
    assert fail[33:86] == "Username and password are not match! Please try again"
    delay()

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except:
        not_found = True

    assert not_found

    #yield
    delay()
    driver.quit()
'''
def test_login_page_InvalidPasswordField():
    """
    #GIVEN the login page
    #WHEN the '/login' page is requested (GET) and a invalid password is input (Lower characters than min allowed password length)
    #THEN check that the response is valid and the user is prompt an error message and not logged in
    """

    option = webdriver.ChromeOptions()
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    
    #driver=uc.Chrome(headless=True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("https://securitycrusaders.live/login")
    #driver.get("http://localhost:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    #Input a valid User Name
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys(testuser)

    #Input a invalid Password
    password = driver.find_element(By.ID,"password")
    password.send_keys('adadw')
    delay()

    #Click Sign in button
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user received an error message
    fail = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']").get_attribute("textContent")
    assert fail[33:86] == "Username and password are not match! Please try again"
    delay()

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except:
        not_found = True

    assert not_found

    #yield
    delay()
    driver.quit()
'''
def test_register_page_InvalidUsernameField():
    """
    #GIVEN the register page
    #WHEN the '/register' page is requested (POST) and a invalid username is input
    #THEN check that the response is valid and the user is not redirected to the dashboard page
    """

    option = webdriver.ChromeOptions()
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    
    #driver=uc.Chrome(headless=True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("https://securitycrusaders.live/register")
    #driver.get("https://localhost:5000/register")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    #Input a Invalid User Name
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys("<script/src=//Ǌ.₨></script>")

    #input valid Email
    email = driver.find_element(By.ID,"email_address")
    email.send_keys(testregisteruser + "@" +testregisteruser + ".com")

    #Input valid Password
    password = driver.find_element(By.ID,"password1")
    password.send_keys(testpassword)

    #Input valid Confirm Password
    password = driver.find_element(By.ID,"password2")
    password.send_keys(testpassword)

    #Click Sign in button
    delay()
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user received an error message
    fail = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div/div/form/div[2]/div/span").get_attribute("textContent")
    assert fail == "[Invalid input.]"
    delay()

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except:
        not_found = True

    assert not_found

    #yield
    delay()
    driver.quit()

def test_register_page_InvalidPasswordField():
    """
    #GIVEN the register page
    #WHEN the '/register' page is requested (POST) and a invalid password and confirm password is input
    #THEN check that the response is valid and the user is not redirected to the dashboard page
    """

    option = webdriver.ChromeOptions()
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    
    #driver=uc.Chrome(headless=True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    driver.maximize_window()
    #driver.get("http://localhost:5000/register")
    driver.get("https://securitycrusaders.live/register")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    #Input a Valid User Name
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys(testregisteruser)

    #input valid Email
    email = driver.find_element(By.ID,"email_address")
    email.send_keys(testregisteruser + "@" +testregisteruser + ".com")

    #Input Invalid Password
    password = driver.find_element(By.ID,"password1")
    password.send_keys('abcd')

    #Input Invalid Confirm Password
    password = driver.find_element(By.ID,"password2")
    password.send_keys('abcd')

    #Click Sign in button
    delay()
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user received an error message
    fail = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div/div/form/div[2]/div/span").get_attribute("textContent")
    assert fail == "[Invalid input.]"
    delay()

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except:
        not_found = True

    assert not_found

    #yield
    delay()
    driver.quit()

'''
def test_register_page():
    """
    #GIVEN the Register page
    #WHEN the user information input to create account is valid (POST)
    #THEN check that the response is valid and the new user account is created and is redirected to the dashboard page
    """

    driver=uc.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("http://localhost:5000/register")

    #For creating new user, increment last number by 1
    temp = testregisteruser
    temp = temp[:-1] + str(int(temp[-1])+1)

    # This for loop scans and searches each line in the file
    # By using the input() method of fileinput module

    with open("data.env", 'r', encoding = 'utf-8') as file:
        filedata = file.read()

    filedata = filedata.replace(testregisteruser, temp)

    with open('data.env', 'w') as file:
        file.write(filedata)


    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    #Input User Name
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys(testregisteruser)

    #input Email
    email = driver.find_element(By.ID,"email_address")
    email.send_keys(testregisteruser + "@" +testregisteruser + ".com")

    #Input Password
    password = driver.find_element(By.ID,"password1")
    password.send_keys(testpassword)

    #Input Confirm Password
    password = driver.find_element(By.ID,"password2")
    password.send_keys(testpassword)

    #Click Sign in button
    delay()
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user is in Dashboard page

    #look for success notification
    #success = driver.find_element(By.CLASS_NAME, "alert alert-success").text
    #assert success[0-29] == "Success! You are logged in as:"

    #time.sleep(random.randint(4,5))
    #success = driver.find_element(By.XPATH, "//div[@class='alert alert-success']").get_attribute("innertext")
    success = driver.find_element(By.XPATH, "//div[@class='alert alert-success']").get_attribute("textContent")
    success = success[33:88]
    print ("success = success[33:88] is" + success)
    assert success == "Account created successfully! You are now logged in as "

    #yield
    delay()
    driver.quit()
    
'''
'''
from msilib import type_string, type_valid
from application.models import User, employment, industry, unienrolment

'''
'''
def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email_address and password_hash fields are defined correctly
    """

    user = User (10, "testing", "testing@test.com", "123abcTEST")
    assert user.id == 10
    assert user.username == "testing"
    assert user.email_address == "testing@test.com"
    assert user.password_hash != "123abcTEST"
'''
'''
def test_new_employment():
    """
    GIVEN a employment model
    WHEN a new employment is created
    THEN check the year, schoolName, degName, employmentRate, salary, industry are defined correctly
    """

    employmentObj = employment(2, "SIT", "Information Security", 90.05, 5500, "IT")
    assert employmentObj.year == 2
    assert employmentObj.schoolName == "SIT"
    assert employmentObj.degName == "Information Security"
    assert employmentObj.employmentRate == 90.05
    assert employmentObj.salary == 5500
    assert employmentObj.industry == "IT"


def test_new_industry():
    """
    GIVEN a industry model
    WHEN a new industry is created
    THEN check the industryName, vacancy and, year are defined correctly
    """

    industryObj = industry("IT", 5, 2)
    assert industryObj.industryName == "IT"
    assert industryObj.vacancy == 5
    assert industryObj.year == 2

def test_new_unienrolment():
    """
    GIVEN a unienrolment model
    WHEN a new unienrolment is created
    THEN check the uniId, industry, year, intake, enrolment and, graduates are defined correctly
    """

    unienrolmentObj = unienrolment(5, "IT", 2, 80, 70, 60)
    assert unienrolmentObj.uniId == 5
    assert unienrolmentObj.industry == "IT"
    assert unienrolmentObj.year == 2
    assert unienrolmentObj.intake == 80
    assert unienrolmentObj.enrolment == 70
    assert unienrolmentObj.graduates == 60

'''