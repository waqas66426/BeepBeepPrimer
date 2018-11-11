from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    firstname = f.StringField('firstname')
    lastname = f.StringField('lastname')
    password = f.PasswordField('password')
    age = f.IntegerField('age')
    weight = f.FloatField('weight')
    max_hr = f.IntegerField('max_hr')
    rest_hr = f.IntegerField('rest_hr')
    vo2max = f.FloatField('vo2max')

    display = ['email', 'firstname', 'lastname', 'password',
               'age', 'weight', 'max_hr', 'rest_hr', 'vo2max']

class PlanForm(FlaskForm):
    start_date = f.DateField('Start date (YYYY-mm-dd)')
    end_date = f.DateField('End date (YYYY-mm-dd)')
    distance = f.IntegerField('Kilometers to run')

    display = ['start_date', 'end_date', 'distance']

class ReportForm(FlaskForm):
    frequency = f.SelectField('frequency', choices = [('15', '15s'), ('30', '30s'), ('60', '1m'), ('300', '5m'),
                                                      ('3600', '1h'), ('28800', '8h'), ('86400', '24h')])
    display = ['frequency']

