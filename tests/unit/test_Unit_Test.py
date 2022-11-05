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


def test_login_page_InvalidUsernameField():
    """
    #GIVEN the login page
    #WHEN the '/login' page is requested (POST) with a invalid username and a valid password is send
    #THEN check that the response is valid and the user is prompt an error message and not logged in
    """

    option = webdriver.ChromeOptions()

    #Comment these 2 to run locally
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')

    option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    #driver.maximize_window()
    driver.get("http://localhost:5000/login")
    #driver.get("http://securitycrusaders:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    try:
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
        failWarning = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div/div/form/div[2]/div/span").get_attribute("textContent")
        delay()
        assert failWarning == "[Invalid input.]"
        delay()

    except NoSuchElementException():
        fail = False
        assert fail
    

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except NoSuchElementException:
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

    #Comment these 2 to run locally
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')

    option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    #driver.maximize_window()
    driver.get("http://localhost:5000/login")
    #driver.get("http://securitycrusaders:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)
    try:
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
        failWarning = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']").get_attribute("textContent")
        assert failWarning[33:86] == "Username and password are not match! Please try again"
        delay()
    except NoSuchElementException:
        fail = False
        assert fail

    #Check if user received an error message
    #fail = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']").get_attribute("textContent")
    #assert fail[33:86] == "Username and password are not match! Please try again"
    #delay()

    #Check if user is in Dashboard page
    try:
        driver.find_element(By.XPATH, "//a[@class='nav-link']")
        not_found = False
    except NoSuchElementException:
        not_found = True

    assert not_found

    #yield
    delay()
    driver.quit()

def test_login_page_InvalidPasswordField():
    """
    #GIVEN the login page
    #WHEN the '/login' page is requested (GET) and a invalid password is input (Lower characters than min allowed password length)
    #THEN check that the response is valid and the user is prompt an error message and not logged in
    """

    option = webdriver.ChromeOptions()
    
    #Comment these 2 to run locally
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')
    
    option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    #driver.maximize_window()
    driver.get("https://securitycrusaders.live/login")
    #driver.get("http://localhost:5000/login")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    try:
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
        #fail = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']").get_attribute("textContent")
        #assert fail[33:86] == "Username and password are not match! Please try again"
        #delay()
        failWarning = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div/div/form/div[3]/div/span").get_attribute("textContent")
        delay()
        assert failWarning == "[Field must be at least 8 characters long.]"
        delay()

    except NoSuchElementException:
        fail = False
        assert fail

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

def test_register_page_InvalidUsernameField():
    """
    #GIVEN the register page
    #WHEN the '/register' page is requested (POST) and a invalid username is input
    #THEN check that the response is valid and the user is not redirected to the dashboard page
    """

    #For creating new user, increment last number by 1
    global testregisteruser
    temp = testregisteruser
    if temp[-2] != '0':
        temp = temp[:-2] + str(int(temp[-2:])+1)
    else:
        temp = temp[:-1] + str(int(temp[-1])+1)
    # This for loop scans and searches each line in the file
    # By using the input() method of fileinput module

    with open("data.env", 'r', encoding = 'utf-8') as file:
        filedata = file.read()

    filedata = filedata.replace(testregisteruser, temp)
    testregisteruser = temp

    with open('data.env', 'w') as file:
        file.write(filedata)

    option = webdriver.ChromeOptions()

    #Comment these 2 to run locally
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')

    option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    #driver.maximize_window()
    #driver.get("https://securitycrusaders.live/register")
    driver.get("http://localhost:5000/register")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    try:
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

    except NoSuchElementException:
        fail = False
        assert fail

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

def test_register_page_InvalidEmailField():
    """
    #GIVEN the register page
    #WHEN the '/register' page is requested (POST) and a invalid email is input
    #THEN check that the response is valid and the user is not redirected to the dashboard page
    """

    #For creating new user, increment last number by 1
    global testregisteruser
    temp = testregisteruser
    if temp[-2] != '0':
        temp = temp[:-2] + str(int(temp[-2:])+1)

    else:
        temp = temp[:-1] + str(int(temp[-1])+1)
    # This for loop scans and searches each line in the file
    # By using the input() method of fileinput module

    with open("data.env", 'r', encoding = 'utf-8') as file:
        filedata = file.read()

    filedata = filedata.replace(testregisteruser, temp)
    testregisteruser = temp

    with open('data.env', 'w') as file:
        file.write(filedata)

    option = webdriver.ChromeOptions()

    #Comment these 2 to run locally
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')

    option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    #driver.maximize_window()
    driver.get("http://localhost:5000/register")
    #driver.get("https://securitycrusaders.live/register")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #recaptcha(driver)

    try:
        #Input a Valid User Name
        user_name = driver.find_element(By.ID,"username")
        user_name.send_keys(testregisteruser)

        #input Invalid Email
        email = driver.find_element(By.ID,"email_address")
        email.send_keys(testregisteruser + "@" +testregisteruser)

        #Input Valid Password
        password = driver.find_element(By.ID,"password1")
        password.send_keys('abcdefgh')

        #Input Valid Confirm Password
        password = driver.find_element(By.ID,"password2")
        password.send_keys('abcdefgh')

        #Click Sign in button
        delay()
        driver.find_element(By.ID,"submit").click()
        delay()

        #Check if user received an error message
        fail = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div/div/form/div[3]/div/span").get_attribute("textContent")
        assert fail == "[Invalid input.]"
        delay()
    
    except NoSuchElementException:
        fail = False
        assert fail

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