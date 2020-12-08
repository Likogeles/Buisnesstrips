from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import EmailField


class AddTripForm(FlaskForm):
    city_from = StringField('Откуда', validators=[DataRequired()])
    city_where = StringField('Город', validators=[DataRequired()])
    hostel_time_in = DateField('Дата въезда в отель', validators=[DataRequired()])
    duration = StringField('Продолжительность поездки (в днях)', validators=[DataRequired()])
    description = StringField('Описание поездки', validators=[DataRequired()])

    # hostel = StringField('Хостел', validators=[DataRequired()])
    # hostel_price = StringField('Цена отеля', validators=[DataRequired()])
    # flight_price = StringField('Цена перелёта', validators=[DataRequired()])
    # flight_company = StringField('Авиакомпания', validators=[DataRequired()])
    # departure_time_city = StringField('Время вылета', validators=[DataRequired()])
    # departure_time_home = StringField('Время вылета домой', validators=[DataRequired()])
    # hostel_time_out = StringField('Выезд из отеля', validators=[DataRequired()])

    submit = SubmitField('Добавить')
