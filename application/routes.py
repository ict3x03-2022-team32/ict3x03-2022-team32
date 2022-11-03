# from werkzeug.wrappers import request
import os
from os import write

import re
from application import app
from flask import render_template, url_for, redirect,flash, get_flashed_messages, request, Response
from application.form import UserDataForm, RegisterForm, LoginForm, Form, EmploymentDataForm, IndustryDataForm, EnrolmentDataForm

from application.models import DecimalEncoder, employment, IncomeExpenses, User, Degree, University, industry, unienrolment
from application import db
import json
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from sqlalchemy.sql.expression import distinct
from operator import and_

from application.form import UploadForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from werkzeug.utils import secure_filename
import pandas as pd
from pyparsing import *
from application import limiter

import pymysql

import io
from io import StringIO 
import csv
from csv import writer

ALLOWED_EXTENSIONS = {'txt', 'csv'}
script_dir = os.path.dirname(__file__)
rel_path = "..\\tempFileUploadDir\\"
UPLOAD_FOLDER = os.path.join(script_dir, rel_path)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.errorhandler(429)
def ratelimit_handler(e):
  return "You have exceeded your rate-limit"

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/index' , methods=['GET', 'POST'])
@login_required
def index():
    form = Form()
    form.uname.choices = [(uni.uname) for uni in University.query.order_by(University.uId).all() ]
    form.degName.choices =  [(degree.degName) for degree in Degree.query.order_by(Degree.degId).all() ]
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html', entries = entries, form=form)

@app.route('/employment' , methods=['GET', 'POST'])
@login_required
def employments():
    form = Form()
    form.degName.choices =  [(degree.degName) for degree in Degree.query.order_by(Degree.degId).all() ]
    entries = employment.query.filter_by(industry = form.degName.choices[0])
    if request.method == "POST":
        if form.degName.data == "Healthcare":
            entries = employment.query.filter_by(industry = form.degName.choices[1])
            return render_template('employment.html', entries = entries, form=form)
        if form.degName.data == "Engineering":
            entries = employment.query.filter_by(industry = form.degName.choices[2])
            return render_template('employment.html', entries = entries, form=form)
        if form.degName.data == "Business":
            entries = employment.query.filter_by(industry = form.degName.choices[3])
            return render_template('employment.html', entries = entries, form=form)
        if form.degName.data == "Arts":
            entries = employment.query.filter_by(industry = form.degName.choices[4])
            return render_template('employment.html', entries = entries, form=form)        
    return render_template('employment.html', entries = entries, form=form)


@app.route('/industry' , methods=['GET', 'POST'])
@login_required
def industry2():
    form = Form()
    form.degName.choices =  [(degree.degName) for degree in Degree.query.order_by(Degree.degId).all() ]
    entries = industry.query.filter_by(industryName = form.degName.choices[0])
    if request.method == "POST":
            if form.degName.data == "Healthcare":
                entries = industry.query.filter_by(industryName = form.degName.choices[1])
                return render_template('industry.html', entries = entries, form=form)
            if form.degName.data == "Engineering":
                entries = industry.query.filter_by(industryName = form.degName.choices[2])
                return render_template('industry.html', entries = entries, form=form)
            if form.degName.data == "Business":
                entries = industry.query.filter_by(industryName = form.degName.choices[3])
                return render_template('industry.html', entries = entries, form=form)
            if form.degName.data == "Arts":
                entries = industry.query.filter_by(industryName = form.degName.choices[4])
                return render_template('industry.html', entries = entries, form=form)      
    return render_template('industry.html', entries = entries, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('dashboard'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)




@app.route('/add', methods = ["POST", "GET"])
@login_required
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data, category=form.category.data, amount=form.amount.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"{form.type.data} has been added to {form.type.data}s", "success")
        return redirect(url_for('employment'))
    return render_template('add.html', title="Add expenses", form=form)
    


@app.route('/addEmployment', methods = ["POST", "GET"])
@login_required
def add_employment():
    form = EmploymentDataForm()
    if request.method == "POST":
        if form.validate_on_submit():
            year = request.form['year']
            schoolName = request.form['schoolName']
            degName = request.form['degName']
            employmentRate = request.form['employmentRate']
            salary = request.form['salary']
            industry = request.form['industry']
            entry = employment(year,schoolName,degName,employmentRate,salary,industry)

            db.session.add(entry)
            db.session.commit()
            flash(f"Data has been added to Employment Data", "success")
            return redirect(url_for('employment'))
    return render_template('addEmployment.html', title="Add Employment Data", form=form)


@app.route('/addIndustry', methods = ["POST", "GET"])
@login_required
def add_industry():
    form = IndustryDataForm()
    if request.method == "POST":
        if form.validate_on_submit():
            industryName = request.form['industryName']
            vacancy = request.form['vacancy']
            year = request.form['year']
            entry = industry(industryName,vacancy,year)
            db.session.add(entry)
            db.session.commit()
            flash(f"Data has been added to Industry Data", "success")
            return redirect(url_for('industry2'))
    return render_template('addIndustry.html', title="Add Industry Data", form=form)








@app.route('/update', methods = ['GET', 'POST'])
def update():
        if request.method == "POST":
                entry = IncomeExpenses.query.get(request.form.get('id'))
                entry.type = request.form['type']
                entry.email = request.form['category']
                entry.phone = request.form['amount']
                entry.date = request.form['date']
                db.session.commit()
                flash("Data Updated Successfully")
                return redirect(url_for('index'))
        return redirect(url_for('index'))



@app.route('/update2', methods = ['GET', 'POST'])
def update2():
        if request.method == "POST":
            entry = employment.query.get(request.form.get('id'))            
            entry.year = request.form['year']
            entry.schoolName = request.form['schoolName']
            entry.degName = request.form['degName']
            entry.employmentRate = request.form['employmentRate']
            entry.salary = request.form['salary']
            entry.industry = request.form['industry']
            db.session.commit()
            flash("Data Updated Successfully")
 
        return redirect(url_for('employment'))


@app.route('/update3', methods = ['GET', 'POST'])
def update3():
        if request.method == "POST":
            entry = industry.query.get(request.form.get('id'))            
            entry.industryName = request.form['industryName']
            entry.vacancy = request.form['vacancy']
            entry.year = request.form['year']
            db.session.commit()
            flash("Data Updated Successfully")
 
        return redirect(url_for('industry2'))



@app.route('/delete-post/<int:entry_id>')
@login_required
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("index"))


@app.route('/delete2-post/<int:entry_id>')
@login_required
def delete2(entry_id):
    entry = employment.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("employment"))


@app.route('/delete3-post/<int:entry_id>')
@login_required
def delete3(entry_id):
    entry = industry.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("industry2"))


@app.route('/download/report/csv')
@login_required
def download():
    def without_keys(d, keys):
        return {x: d[x] for x in d if x not in keys}


    emp = employment.query.order_by(employment.geid.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)



    for u in emp:
        print ()
        invalid = {"_sa_instance_state","geid"}
        y = without_keys(u.__dict__,invalid)
        writer.writerow(y.values())
    output.seek(0)
    return Response(output,mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employment_report.csv"})




@app.route('/download1/report/csv')
@login_required
def download1():
    def without_keys(d, keys):
        return {x: d[x] for x in d if x not in keys}


    ind = industry.query.order_by(industry.industryId.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)

    for u in ind:
        print ()
        invalid = {"_sa_instance_state","industryId"}
        y = without_keys(u.__dict__,invalid)
        writer.writerow(y.values())
    output.seek(0)
    return Response(output,mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=industry_report.csv"})



@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


#------------------------Dash board Functions (Use SQL queries to retreive and analyse data )------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    #Pie chart: Industry vacancy in latest year
    #MAX year
    #SELECT MAX(year) FROM industry
    max_year = db.session.query(db.func.max(industry.year))

    #SELECT I.industryName, I.vacancy FROM industry I WHERE I.year = (SELECT MAX(year) FROM industry);
    industry_vacancy_data = db.session.query(industry.vacancy, industry.industryName).filter(industry.year == max_year).all()
    industry_vacancy = []
    industry_industryName = []
    for vacancy, industryName in industry_vacancy_data:
        industry_vacancy.append(vacancy)
        industry_industryName.append(industryName)

    #Pie chart:Industry graduates in over the years
    #SELECT i.industryName, SUM(u.graduates) FROM uniEnrolment u INNER JOIN industry i ON u.industry = i.industryName GROUP BY i.industryName;
    industry_graduate_data = db.session.query(industry.industryName, db.func.sum(unienrolment.graduates)).select_from(unienrolment).join(industry, unienrolment.industry == industry.industryName).group_by(industry.industryName)
    industry_graduates = []
    industry_graduates_label = []
    for industry_name, graduates in industry_graduate_data:
        industry_graduates_label.append(industry_name)
        industry_graduates.append(graduates)
    
    #Line chart: Average salary based on industry total 5 lines over the years
    #SELECT DISTINCT industry FROM employment;
    employment_industry_data = db.session.query( distinct(employment.industry))
    employment_industry = []
    for industry_name in employment_industry_data:
        employment_industry.append(industry_name[0])
    
    #SELECT ROUND(AVG(salary)), year FROM employment WHERE industry = 'Arts' GROUP BY year
    employment_salary_arts_data = db.session.query(db.func.round(db.func.avg(employment.salary), 2), employment.year).filter(employment.industry == "Arts").group_by(employment.year)
    employment_salary_arts = []
    employment_year = []
    for avg_salary, year in employment_salary_arts_data:
        employment_salary_arts.append(avg_salary)
        employment_year.append(year)

    #SELECT ROUND(AVG(salary)) FROM employment WHERE industry = 'Business' GROUP BY year
    employment_salary_business_data = db.session.query(db.func.round(db.func.avg(employment.salary))).filter(employment.industry == "Business").group_by(employment.year)
    employment_salary_business = []
    for avg_salary in employment_salary_business_data:
        employment_salary_business.append(avg_salary[0])

    #SELECT ROUND(AVG(salary)) FROM employment WHERE industry = 'Engineering' GROUP BY year
    employment_salary_engineering_data = db.session.query(db.func.round(db.func.avg(employment.salary))).filter(employment.industry == "Engineering").group_by(employment.year)
    employment_salary_engineering = []
    for avg_salary in employment_salary_engineering_data:
        employment_salary_engineering.append(avg_salary[0])

    #SELECT ROUND(AVG(salary)) FROM employment WHERE industry = 'Healthcare' GROUP BY year
    employment_salary_Healthcare_data = db.session.query(db.func.round(db.func.avg(employment.salary))).filter(employment.industry == "Healthcare").group_by(employment.year)
    employment_salary_Healthcare = []
    for avg_salary in employment_salary_Healthcare_data:
        employment_salary_Healthcare.append(avg_salary[0])

    #SELECT ROUND(AVG(salary)) FROM employment WHERE industry = 'ICT' GROUP BY year
    employment_salary_ICT_data = db.session.query(db.func.round(db.func.avg(employment.salary))).filter(employment.industry == "ICT").group_by(employment.year)
    employment_salary_ICT = []
    for avg_salary in employment_salary_ICT_data:
        employment_salary_ICT.append(avg_salary[0])

    #Bar chart: ICT 5 bars
    #SELECT I.year, I.industryName, C.graduates, I.vacancy FROM uniEnrolment C, industry I WHERE C.industry = I.industryName AND C.year = I.year AND C.industry = "ICT";
    unienrolment_ICT_data = db.session.query(industry.year, industry.industryName, unienrolment.graduates, industry.vacancy, unienrolment.intake, unienrolment.enrolment).select_from(unienrolment).join(industry, unienrolment.industry == industry.industryName).filter( and_(unienrolment.year == industry.year, unienrolment.industry == "ICT")).all()
    industry_year = []
    industry_unienrolment_industry = []
    unienrolment_graduates = []
    industry_unienrolment_vacancy = []
    unienrolment_intake = []
    unienrolment_enrolment = []
    for year, industry_name, gratuates, vacancy, intake, enrolment in unienrolment_ICT_data:
        industry_year.append(year)
        industry_unienrolment_industry.append(industry_name)
        unienrolment_graduates.append(gratuates)
        industry_unienrolment_vacancy.append(vacancy)
        unienrolment_intake.append(intake)
        unienrolment_enrolment.append(enrolment)
    
    #SELECT C.graduates, I.vacancy FROM uniEnrolment C, industry I WHERE C.industry = I.industryName AND C.year = I.year AND C.industry = "Business";
    unienrolment_Business_data = db.session.query(unienrolment.graduates, industry.vacancy, unienrolment.intake, unienrolment.enrolment).select_from(unienrolment).join(industry, unienrolment.industry == industry.industryName).filter(and_(unienrolment.year == industry.year, unienrolment.industry == "Business")).all()
    unienrolment_business_graduates = []
    industry_unienrolment_business_vacancy = []
    unienrolment_business_intake = []
    unienrolment_business_enrolment = []
    for gratuates, vacancy, intake, enrolment in unienrolment_Business_data:
        unienrolment_business_graduates.append(gratuates)
        industry_unienrolment_business_vacancy.append(vacancy)
        unienrolment_business_intake.append(intake)
        unienrolment_business_enrolment.append(enrolment)

    #SELECT C.graduates, I.vacancy FROM uniEnrolment C, industry I WHERE C.industry = I.industryName AND C.year = I.year AND C.industry = "Engineering";
    unienrolment_engineering_data = db.session.query(unienrolment.graduates, industry.vacancy, unienrolment.intake, unienrolment.enrolment).select_from(unienrolment).join(industry, unienrolment.industry == industry.industryName).filter(and_(unienrolment.year == industry.year, unienrolment.industry == "Engineering")).all()
    unienrolment_engineering_graduates = []
    industry_unienrolment_engineering_vacancy = []
    unienrolment_engineering_intake = []
    unienrolment_engineering_enrolment = []
    for gratuates, vacancy, intake, enrolment in unienrolment_engineering_data:
        unienrolment_engineering_graduates.append(gratuates)
        industry_unienrolment_engineering_vacancy.append(vacancy)
        unienrolment_engineering_intake.append(intake)
        unienrolment_engineering_enrolment.append(enrolment)

    #SELECT C.graduates, I.vacancy FROM uniEnrolment C, industry I WHERE C.industry = I.industryName AND C.year = I.year AND C.industry = "Healthcare";
    unienrolment_healthcare_data = db.session.query(unienrolment.graduates, industry.vacancy, unienrolment.intake, unienrolment.enrolment).select_from(unienrolment).join(industry, unienrolment.industry == industry.industryName).filter(and_(unienrolment.year == industry.year, unienrolment.industry == "Healthcare")).all()
    unienrolment_healthcare_graduates = []
    industry_unienrolment_healthcare_vacancy = []
    unienrolment_healthcare_intake = []
    unienrolment_healthcare_enrolment = []
    for gratuates, vacancy, intake, enrolment in unienrolment_healthcare_data:
        unienrolment_healthcare_graduates.append(gratuates)
        industry_unienrolment_healthcare_vacancy.append(vacancy)
        unienrolment_healthcare_intake.append(intake)
        unienrolment_healthcare_enrolment.append(enrolment)

    #SELECT C.graduates, I.vacancy FROM uniEnrolment C, industry I WHERE C.industry = I.industryName AND C.year = I.year AND C.industry = "Arts";
    unienrolment_arts_data = db.session.query(unienrolment.graduates, industry.vacancy, unienrolment.intake, unienrolment.enrolment).select_from(unienrolment).join(industry, unienrolment.industry == industry.industryName).filter(and_(unienrolment.year == industry.year, unienrolment.industry == "Arts")).all()
    unienrolment_arts_graduates = []
    industry_unienrolment_arts_vacancy = []
    unienrolment_arts_intake = []
    unienrolment_arts_enrolment = []
    for gratuates, vacancy, intake, enrolment in unienrolment_arts_data:
        unienrolment_arts_graduates.append(gratuates)
        industry_unienrolment_arts_vacancy.append(vacancy)
        unienrolment_arts_intake.append(intake)
        unienrolment_arts_enrolment.append(enrolment)

    #Bar line: Employment rate vs salary for 2019
    #SELECT E.industry, ROUND(AVG(E.employmentRate), 2), ROUND(AVG(E.salary), 2) FROM employment E WHERE E.year = (SELECT MAX(year) FROM industry) GROUP BY E.industry;
    employment_vs_salary_data = db.session.query(db.func.round(db.func.avg(employment.employmentRate), 2), db.func.round(db.func.avg(employment.salary), 2)).filter(employment.year == max_year).group_by(employment.industry)
    avg_employmentrate = []
    avg_salary = []
    for employmentrate, salary in employment_vs_salary_data:
        avg_employmentrate.append(employmentrate)
        avg_salary.append(salary)

    #Two line: Avg (Employment rate), graduates for 2019 for all industry
    #SELECT E.industry, ROUND(AVG(E.employmentRate), 2), U.graduates FROM employment E, uniEnrolment U WHERE U.year = E.year AND U.industry = E.industry AND E.year = (SELECT MAX(year) FROM industry) GROUP BY E.industry;
    employmentrate_vs_graduates_data = db.session.query(db.func.round(db.func.avg(employment.employmentRate),2), unienrolment.graduates).select_from(employment).join(unienrolment, unienrolment.industry == employment.industry).filter(employment.year == max_year).group_by(employment.industry)
    
    avg_unienrolment_employmentRate = []
    unienrolment_employment_graduates = []
    for employmentrate, graduates in employmentrate_vs_graduates_data:
        avg_unienrolment_employmentRate.append(employmentrate)
        unienrolment_employment_graduates.append(graduates)


    return render_template('dashboard.html',
                            industry_vacancy = json.dumps(industry_vacancy),
                            industry_industryName = json.dumps(industry_industryName),
                            employment_industry = json.dumps(employment_industry),
                            employment_salary_arts = json.dumps(employment_salary_arts, cls=DecimalEncoder),                    #added , cls=DecimalEncoder
                            employment_year = json.dumps(employment_year),
                            industry_year = json.dumps(industry_year),
                            industry_unienrolment_industry = json.dumps(industry_unienrolment_industry),
                            unienrolment_graduates = json.dumps(unienrolment_graduates),
                            industry_unienrolment_vacancy = json.dumps(industry_unienrolment_vacancy),
                            unienrolment_intake = json.dumps(unienrolment_intake),
                            unienrolment_enrolment = json.dumps(unienrolment_enrolment),
                            avg_employmentrate = json.dumps(avg_employmentrate),
                            avg_salary = json.dumps(avg_salary, cls=DecimalEncoder),                                            #added , cls=DecimalEncoder
                            avg_unienrolment_employmentRate = json.dumps(avg_unienrolment_employmentRate),
                            unienrolment_employment_graduates = json.dumps(unienrolment_employment_graduates),
                            employment_salary_business = json.dumps(employment_salary_business, cls=DecimalEncoder),            #added , cls=DecimalEncoder
                            employment_salary_engineering = json.dumps(employment_salary_engineering, cls=DecimalEncoder),      #added , cls=DecimalEncoder
                            employment_salary_Healthcare = json.dumps(employment_salary_Healthcare, cls=DecimalEncoder),        #added , cls=DecimalEncoder
                            employment_salary_ICT = json.dumps(employment_salary_ICT, cls=DecimalEncoder),                      #added , cls=DecimalEncoder
                            unienrolment_business_graduates = json.dumps(unienrolment_business_graduates),
                            industry_unienrolment_business_vacancy = json.dumps(industry_unienrolment_business_vacancy),
                            unienrolment_business_intake = json.dumps(unienrolment_business_intake),
                            unienrolment_business_enrolment = json.dumps(unienrolment_business_enrolment),
                            unienrolment_engineering_graduates = json.dumps(unienrolment_engineering_graduates),
                            industry_unienrolment_engineering_vacancy = json.dumps(industry_unienrolment_engineering_vacancy),
                            unienrolment_engineering_intake = json.dumps(unienrolment_engineering_intake),
                            unienrolment_engineering_enrolment = json.dumps(unienrolment_engineering_enrolment),
                            unienrolment_healthcare_graduates = json.dumps(unienrolment_healthcare_graduates),
                            industry_unienrolment_healthcare_vacancy = json.dumps(industry_unienrolment_healthcare_vacancy),
                            unienrolment_healthcare_intake = json.dumps(unienrolment_healthcare_intake),
                            unienrolment_healthcare_enrolment = json.dumps(unienrolment_healthcare_enrolment),
                            unienrolment_arts_graduates = json.dumps(unienrolment_arts_graduates),
                            industry_unienrolment_arts_vacancy = json.dumps(industry_unienrolment_arts_vacancy),
                            unienrolment_arts_intake = json.dumps(unienrolment_arts_intake),
                            unienrolment_arts_enrolment = json.dumps(unienrolment_arts_enrolment),
                            industry_graduates = json.dumps(industry_graduates, cls=DecimalEncoder),                            #added , cls=DecimalEncoder
                            industry_graduates_label = json.dumps(industry_graduates_label)
    )

#------------------------Upload CSV file function (to upload dataset into database)------------------------------------#

def check_IfAllowedFile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def try_utf8(data):
    "Returns a Unicode object on success, or None on failure"
    try:
       return data.decode('utf-8')
    except UnicodeDecodeError:
       return None

def check_IfEmpty(file):
    try:
        content = open(file, 'r').read()
        if re.search(r'^\s*$', content):
            return True
        udata = try_utf8(content)
        if udata is None:
            return True
        else:
            return False
    except:
        return False
    
def check_IfBinaryFile(filepathname):
    textchars = bytearray([7,8,9,10,12,13,27]) + bytearray(range(0x20, 0x7f)) + bytearray(range(0x80, 0x100))
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    if is_binary_string(open(filepathname, 'rb').read(1024)):
       return True
    else:
       return False

def check_FileData(filename):
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            if not re.match("^(\d{4}),([\w\s\&\-\(\)]{1,60}),([\w\s\&\-\(\)\#\^]{1,255}),([+-]?(?:[0-9]*[.])?[0-9]+),(\d{1,10}),([\w\s\&\-\(\)]{1,255})$" , line):
                return False
        return True
    except:
        return False

def get_Fileobjectsize(fobj):
    if fobj.content_length:
        return fobj.content_length

    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  #seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  #assume small enough

@app.route('/upload', methods=['GET', 'POST'])
# @login_required
# @rbac.allow(['administrator'], methods=['GET', 'POST'])
@limiter.limit("30/minute")
def upload():

    form = UploadForm()

    if form.validate_on_submit():
        f = form.upload.data
        #app.logger.warning('%s attempted to upload a file ', current_user.username)
        # Check if request body for form.upload.data is too large
        if get_Fileobjectsize(f) < 1 * (1024 ** 2) and check_IfAllowedFile(f.filename):
            filename = secure_filename(f.filename)
            print (filename)
            fullFileName = os.path.join(UPLOAD_FOLDER, filename)
            f.save(fullFileName)
            # Check if file is a binary or text file
            if check_IfBinaryFile(fullFileName):
                flash('File is not a csv/txt file')
                #app.logger.warning('%s uploaded a binary file and not a file containing text data', current_user.username)
                os.remove(fullFileName)
                return render_template('uploadDataset.html', form=form)
            # Check if file is empty or file size is too large
            if check_IfEmpty(fullFileName) or (os.stat(fullFileName).st_size > 1 * (1024 ** 2)):
                flash ("File is either empty or too large")
                #app.logger.warning('%s uploaded a file that is either empty or too large', current_user.username)
                os.remove(fullFileName)
            else:
                # Check if data format in CSV/txt file follows a certain format
                if check_FileData(fullFileName) :
                    return insertDataset(fullFileName)
                else:
                    flash ("CSV File format is incorrect")
                    #app.logger.warning('%s uploaded a file that does not follow dataset format', current_user.username)
                    os.remove(fullFileName)
        else:
            #app.logger.warning('%s uploaded a file whose size is either too big or file whose extension is not allowed', current_user.username)
            flash('File size is either too big or file extension is not allowed')
    return render_template('uploadDataset.html', form=form)
def insertDataset(fullFileName):
    # CVS Column Names
    col_names = ['year','schoolName','degName','employmentRate','salary','industry']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(fullFileName, names=col_names, header=None)
    
    # Try insert data from csv into dataset and catch if dataset cannot be inserted
    try:
        # Loop through the Rows
        for i,row in csvData.iterrows():
            newEmployement = employment(year = row['year'], 
            schoolName = row['schoolName'], 
            degName = row['degName'] , 
            employmentRate = row['employmentRate'] , 
            salary = row['salary'], 
            industry = row['industry'])
            db.session.add(newEmployement)   
            db.session.commit()
    except:
        # Remove file after unsuccessful data upload
        os.remove(fullFileName)
        #app.logger.warning('%s was not successful in uploading dataset into database', current_user.username)
        flash('Dataset was not fully inserted successfully, please contact the database admin for help')
        return redirect(url_for('admin_HomePage'))
    
    db.session.close()
    # Remove file after successful data upload
    os.remove(fullFileName)
    #app.logger.warning('%s successfully uploaded dataset into database', current_user.username)
    flash('Dataset Successfully uploaded')
    return redirect(url_for('admin_HomePage'))

@app.route('/adminhomepage')
# @login_required
# @rbac.allow(['administrator'], methods=['GET', 'POST'])
def admin_HomePage():
    return render_template('adminHomepage.html')


@app.route('/download', methods=['GET'])
# @login_required
# @rbac.allow(['administrator'], methods=['GET'])
@limiter.limit("240/minute")
def fileDownload():
    return render_template('downloadDataset.html')


@app.route('/download/report/csv', methods=['GET'])
# @login_required
# @rbac.allow(['administrator'], methods=['GET'])
@limiter.limit("30/minute")
def download_report():
	conn = None
	cursor = None
	try:
		conn = db.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		
		cursor.execute("SELECT year,schooName,degName, employmentRate, salary, industry FROM employment")
		result = cursor.fetchall()

		output = io.StringIO()
		writer = csv.writer(output)
		
		line = ['year,schooName,degName, employmentRate, salary, industry']
		writer.writerow(line)

		for row in result:
			line = [str(row['year']),row['schooName'],row['degName'], str(row['employmentRate']), str(row['salary']), row['industry']]
			writer.writerow(line)

		output.seek(0)
		#app.logger.warning('%s downloaded a copy of the data from the database', current_user.username)
		return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()