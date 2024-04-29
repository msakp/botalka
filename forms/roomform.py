import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, IntegerField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    name = StringField('Спецификация Бота', validators=[DataRequired()])
    timelimit = IntegerField("Время Бота",
                          validators=[DataRequired()],
                          default=60)
    submit = SubmitField('Создать')
