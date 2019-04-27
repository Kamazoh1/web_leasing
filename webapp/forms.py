from flask_wtf import FlaskForm
#https://flask-wtf.readthedocs.io/ 
#https://www.tutorialspoint.com/flask/flask_wtf.htm - с перечислением типов
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextField, TextAreaField, DecimalField, SelectField
#импортируем типы полей 
from wtforms.validators import DataRequired, Email, NumberRange
from webapp.model import ANN_TYPE, GENDER, ROLE, Tool
from wtforms_sqlalchemy.fields import QuerySelectField
#validator - класс, который помогает избежать ручных проверок
#DataRequired - проверяет, что пользователь действительно вбил данные


class RegistrationForm (FlaskForm): #наследуем форму от FlaskForm
    name=StringField('Имя пользователя', validators=[DataRequired('Введите имя')])
    surname=StringField('Фамилия пользователя', validators=[DataRequired('Введите фамилию')])
    password=PasswordField('Пароль', validators=[DataRequired('Какой вы хотите себе пароль?')])
    email=StringField('Адрес эл.почты', validators=[DataRequired('Какой у вас адрес электронной почты?'), Email('Тут нужен адрес электронной почты')])
    gender=RadioField('Пол', choices=GENDER, validators=[DataRequired('Какого вы пола?')])
    submit=SubmitField('Зарегистрироваться')


class LoginForm (FlaskForm):
    email=StringField('Ваш адрес электронной почты:', validators=[DataRequired('Укажите Ваш адрес эл.почты')])
    password=PasswordField('Пароль:', validators=[DataRequired('Введите Ваш пароль')])
    remember=BooleanField('Запомнить', default=False, render_kw={"class":"form_check_input"})
    submit=SubmitField('Зайти')

def announced_tool():
    return Tool.query

def get_pk(obj):
    return str(obj)

class AddAnnouncementForm(FlaskForm): #наследуем форму от FlaskForm
    head=StringField('Название', validators=[DataRequired('Введите название')],render_kw={'class': 'form-control'})
    tool_id=QuerySelectField('Инструмент', query_factory=announced_tool, get_pk=get_pk, get_label='name', allow_blank=True)
    #tool_id=QuerySelectField('Инструмент', query_factory=announced_tool, get_label='Инстр', allow_blank=True)
    type_id=SelectField('Тип', choices=ANN_TYPE, validators=[DataRequired('Нужно выбрать вы хотите сдать или взять в аренду')], render_kw={'class': 'form-control'})
    text=TextAreaField('Детали объявления', validators=[DataRequired('Добавьте деталей, пожалуйста')], render_kw={'class': 'form-control'})
    price=DecimalField('Цена за день', validators=[NumberRange(min=0, message='Укажите стоимость не менее 0')], render_kw={'class': 'form-control'})
    address=StringField('Адрес', validators=[DataRequired('Введите адрес')],render_kw={'class': 'form-control'})

    submit=SubmitField('Создать', render_kw={'class': 'btn btn-primary'})
