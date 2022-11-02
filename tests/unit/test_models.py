from msilib import type_string, type_valid
from application.models import User, employment, industry, unienrolment

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