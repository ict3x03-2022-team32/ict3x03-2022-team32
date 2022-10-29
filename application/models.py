from unicodedata import decimal
from application import db, login_manager
from application import bcrypt
from datetime import datetime
import enum
from flask_login import UserMixin
import json
from decimal import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Degree(db.Model):
    degId = db.Column(db.Integer(), primary_key=True)
    degName = db.Column(db.String(length=60), nullable=False, unique=True)

class University(db.Model):
    uId = db.Column(db.Integer(), primary_key=True)
    uname = db.Column(db.String(length=60), nullable=False, unique=True)

ACCESS = {
    'user': 0,
    'admin': 1
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    isadmin = db.Column(db.Integer)

    def __init__(self, email_address, username, isadmin=ACCESS['user']):
        self.email_address = email_address
        self.username = username
        self.password_hash = ''
        self.isadmin = isadmin

    def is_admin(self):
        return self.isadmin == ACCESS['admin']

    def is_user(self):
        return self.isadmin == ACCESS['user']

    def allowed(self, access_level):
        return self.isadmin >= access_level

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)




class IncomeExpenses(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), default = 'income', nullable=False)
    category = db.Column(db.String(30), nullable=False, default='rent')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    


class employment(db.Model):
    
    geid = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    schoolName = db.Column(db.String(60), nullable=False)
    degName = db.Column(db.String(250), nullable=False)
    employmentRate = db.Column(db.Float, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String(60), nullable=False)

    def __init__(self, year, schoolName, degName, employmentRate, salary, industry):
 
        self.year = year
        self.schoolName = schoolName
        self.degName = degName
        self.employmentRate = employmentRate
        self.salary = salary
        self.industry = industry


class industry(db.Model):
    
    industryId = db.Column(db.Integer, primary_key=True)
    industryName = db.Column(db.String(60), nullable=False)
    vacancy = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, industryName, vacancy, year):
 
        self.industryName = industryName
        self.vacancy = vacancy
        self.year = year


class unienrolment(db.Model):
    
    uniId = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    intake = db.Column(db.Integer, nullable=False)
    enrolment = db.Column(db.Integer, nullable=False)
    graduates = db.Column(db.Integer, nullable=False)
    
    def __init__(self, uniId, industry, year,intake,enrolment,graduates):
 
        self.uniId = uniId
        self.industry = industry
        self.year = year
        self.intake = intake
        self.enrolment = enrolment
        self.graduates = graduates

class comments(db.Model):
    cid = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(60), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cname = db.Column(db.String(60), nullable=False)

    def __init__(self, comment, datetime, cname):
        self.comment = comment
        self.datetime = datetime
        self.cname = cname

#new
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

