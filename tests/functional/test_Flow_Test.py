from flask_login import user_login_confirmed
from dotenv import load_dotenv
import os
import random
import time 
import sys
import fileinput
import pytest


#selenium libraries
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

#recaptcha libraries
#import speech_recognition as sr
#import ffmpy
#import requests
#import urllib
#import pydub


load_dotenv('data.env')

testuser = os.environ.get("testuser")
testpassword = os.environ.get("testpassword")
pub_key = os.environ.get("pub_key")
secret = os.environ.get("private_key")
testregisteruser = os.environ.get("testregisteruser")


##################################################################################################################################################################################    
def delay():
    time.sleep(random.randint(2,3))


def test_index_page():
    ''''''
    #GIVEN the index page
    #WHEN the '/' page is requested (GET)
    #THEN check that the response is valid
    ''''''
    option = webdriver.ChromeOptions()

    #Comment these 2 to run locally
    option.binary_location = "/usr/bin/google-chrome"
    option.add_argument('--headless')

    option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
    driver.implicitly_wait(10)
    #driver.maximize_window()
    driver.get("http://localhost:5000/")
    #driver.get("http://securitycrusaders:5000/")

    #Check title
    title = "Data Analytics for Salary in Industries of Singapore"
    assert title == driver.title

    #yield
    delay()
    driver.quit()


def test_login_page():
    """
    #GIVEN the login page
    #WHEN the '/login' page is requested (POST) with the correct username and password
    #THEN check that the response is valid and the user is redirected to the dashboard page
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

    #Input User Name
    user_name = driver.find_element(By.ID,"username")
    user_name.send_keys(testuser)

    #Input Password
    password = driver.find_element(By.ID,"password")
    password.send_keys(testpassword)
    delay()

    #Click Sign in button
    driver.find_element(By.ID,"submit").click()
    delay()

    #Check if user is in Dashboard page
    success = driver.find_element(By.XPATH, "//div[@class='alert alert-success']").get_attribute("textContent")
    success = success[33:64]
    assert success == "Success! You are logged in as: "

    #yield
    delay()
    driver.quit()

def test_register_page():
    """
    #GIVEN the Register page
    #WHEN the user information input to create account is valid (POST)
    #THEN check that the response is valid and the new user account is created and is redirected to the dashboard page
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
    driver.get("http://localhost:5000/register")

    #For creating new user, increment last number by 1
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
    success = driver.find_element(By.XPATH, "//div[@class='alert alert-success']").get_attribute("textContent")
    success = success[33:88]
    print ("success = success[33:88] is" + success)
    assert success == "Account created successfully! You are now logged in as "

    #yield
    delay()
    driver.quit()
