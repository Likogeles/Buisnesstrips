from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    product_type = SelectField(validators=[DataRequired()])
    search = StringField(validators=[DataRequired()])
