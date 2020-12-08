from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import EmailField


class AddProductForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    number = StringField('Количество', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    product_type = StringField('Тип товара', validators=[DataRequired()])
    # image = FileField("Изображение", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Добавить')
