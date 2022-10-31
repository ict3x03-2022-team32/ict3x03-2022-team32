from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, DataRequired, ValidationError
from application.models import User


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class Form(FlaskForm):
    # state = SelectField('state', choices=[('CA','California'), ('NV', 'Nevada')])
    uname = SelectField('university',choices=[])
    degName = SelectField('degName', choices=[])
    industry = SelectField('industry',choices=[])
    year = SelectField('year',choices=[])
    colour = SelectField('colour',choices=[])


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
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

class EnrolmentDataForm(FlaskForm):
    industryName = SelectField("Industry", validators=[DataRequired()],
                                            choices =['ICT', 'Healthcare',
                                            'Engineering', 'Business',
                                            'Arts'
                                            ]
                            )
    
    year = SelectField('Year', validators=[DataRequired()],choices=['2015', '2016','2017', '2018','2019'])
    intake = IntegerField('Intake', validators = [DataRequired()])
    enrolment = IntegerField('Enrolment', validators = [DataRequired()])
    graduates = IntegerField('Graduates', validators = [DataRequired()])
    submit = SubmitField('Generate Data')             

class EmailResetForm(FlaskForm):
    email_address = EmailField(label='Email Address:', validators=[DataRequired()])

class PasswordResetForm(FlaskForm):
    password =PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
                            