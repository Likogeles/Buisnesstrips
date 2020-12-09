from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import EmailField


class AddTripForm(FlaskForm):
    city_from = StringField('Город отъезда', validators=[Optional()])
    city_where = StringField('Город командировки', validators=[DataRequired()])
    departure_time_city = DateField('Дата вылета', validators=[DataRequired()])
    departure_time_home = DateField('Дата вылета обратно', validators=[DataRequired()])
    description = StringField('Описание поездки', validators=[Optional()])

    # duration = StringField('Продолжительность поездки (в днях)', validators=[DataRequired()])
    # hostel_time_in = DateField('Дата въезда в отель', validators=[DataRequired()])
    # hostel = StringField('Хостел', validators=[DataRequired()])
    # hostel_price = StringField('Цена отеля', validators=[DataRequired()])
    # flight_price = StringField('Цена перелёта', validators=[DataRequired()])
    # flight_company = StringField('Авиакомпания', validators=[DataRequired()])
    # hostel_time_out = StringField('Выезд из отеля', validators=[DataRequired()])

    submit = SubmitField('Оформить в PDF')
