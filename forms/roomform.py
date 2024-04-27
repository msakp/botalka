from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    name = StringField('Спецификация Бота', validators=[DataRequired()])
    submit = SubmitField('Создать')