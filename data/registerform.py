from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    email = EmailField('Логин / Почта', validators=[DataRequired()])
    password1 = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    firstname = StringField('Имя', validators=[DataRequired()])
    secondname = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Зарегестрировать')
