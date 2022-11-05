from xmlrpc.client import DateTime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, DataRequired, ValidationError, Regexp, InputRequired
from application.models import User
import re 
import bleach
#For my (YX) file upload
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), Regexp('^[a-zA-Z0-9_]+([-.][a-zA-Z0-9]+)*$'), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=8),DataRequired()])
    submit = SubmitField(label='Sign in')


class UserDetailForm(FlaskForm):
    id = IntegerField('Id: ')
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Regexp('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'), Email()])
    isadmin = IntegerField('Access: ')
    istimeout = IntegerField('Timed out')
    timeoutTime = DateTime("Time out Date")

class Form(FlaskForm):
    # state = SelectField('state', choices=[('CA','California'), ('NV', 'Nevada')])
    uname = SelectField('university',choices=[])
    degName = SelectField('degName', choices=[])
    industry = SelectField('industry',choices=[])
    year = SelectField('year',choices=[])
    colour = SelectField('colour',choices=[])

class MessageDataForm(FlaskForm):
    def xss_validate_comment(self, comments):
        regex = "(<|%3C)script[\s\S]*?(>|%3E)[\s\S]*?(<|%3C)(\/|%2F)script[\s\S]*?(>|%3E)"
        match = re.search(regex, comments.data)
        if match:
            raise ValidationError("No script tag allowed")
        
    def sql_code_validate(self, comments):
        regex="('(''|[^'])*')|(;)|(\b(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})\b)"
        match = re.search(regex, comments.data)
        if match:
            raise ValidationError("No SQL query allowed")
        
    comments = StringField('Comments', [InputRequired(), xss_validate_comment, sql_code_validate])
    submit = SubmitField('Post Comment')
    
   
    
    


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), Regexp('^[a-zA-Z0-9_]+([-.][a-zA-Z0-9]+)*$'), DataRequired()])
    email_address = EmailField(label='Email Address:', validators=[DataRequired(), Regexp('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    isadmin = IntegerField(label="Access :")
    submit = SubmitField(label='Create Account')
    

class UserDataForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                                choices=[('income', 'income'),
                                        ('expense', 'expense')])
    category = SelectField("Category", validators=[DataRequired()],
                                            choices =[('rent', 'rent'),
                                            ('salary', 'salary'),
                                            ('investment', 'investment'),
                                            ('side_hustle', 'side_hustle')
                                            ]
                            )
    amount = IntegerField('Amount', validators = [DataRequired()])                                   
    submit = SubmitField('Generate Report')



class EmploymentDataForm(FlaskForm):
    year = SelectField('Year', validators=[DataRequired()],
                                choices=['2015', '2016',
                                        '2017', '2018','2019'])
    schoolName = StringField(label='School Name:', validators=[Length(min=2, max=60), DataRequired()])
    degName = StringField(label='Degree Name:', validators=[Length(min=2, max=60), DataRequired()])
    employmentRate = IntegerField('Employment Rate', validators = [DataRequired()])
    salary = IntegerField('Salary', validators = [DataRequired()])
    industry = SelectField("Industry", validators=[DataRequired()],
                                            choices =['ICT', 'Healthcare',
                                            'Engineering', 'Business',
                                            'Arts'
                                            ]
                            )
    submit = SubmitField('Generate Data')


class IndustryDataForm(FlaskForm):
    industryName = SelectField("Industry", validators=[DataRequired()],
                                            choices =['ICT', 'Healthcare',
                                            'Engineering', 'Business',
                                            'Arts'
                                            ]
                            )
    vacancy = IntegerField('Vacancy', validators = [DataRequired()])
    year = SelectField('Year', validators=[DataRequired()],choices=['2015', '2016','2017', '2018','2019'])
    submit = SubmitField('Generate Data')

         

class EmailResetForm(FlaskForm):
    email_address = EmailField(label='Email Address:', validators=[DataRequired(), Regexp('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')])
    submit = SubmitField(label="Submit Email")

class PasswordResetForm(FlaskForm):
    password =PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])    
    submit = SubmitField(label="Submit Password")                                    

class UploadForm(FlaskForm):
        upload = FileField('CSV and TXT only!', validators=[
        FileRequired(),
        FileAllowed(['csv', 'txt'], 'CSV and TXT only!')
    ])

class OTPForm(FlaskForm):
    otp = IntegerField(label="OTP: ")
    submit = SubmitField("Submit OTP")