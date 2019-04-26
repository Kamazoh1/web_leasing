from flask_wtf import FlaskForm
#https://flask-wtf.readthedocs.io/ 
#https://www.tutorialspoint.com/flask/flask_wtf.htm - с перечислением типов
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextField, TextAreaField, DecimalField, SelectField
#импортируем типы полей 
from wtforms.validators import DataRequired, Email, NumberRange
from webapp.model import ANN_TYPE, GENDER, ROLE
#validator - класс, который помогает избежать ручных проверок
#DataRequired - проверяет, что пользователь действительно вбил данные
from webapp.model import GENDER, ANN_TYPE, ROLE


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
<<<<<<< HEAD
    remember=BooleanField('Запомнить', default=True, render_kw={"class":"form_check_input"})
    submit=SubmitField('Зайти')



class AddAnnouncementForm (FlaskForm): #наследуем форму от FlaskForm
    head=StringField('Название', validators=[DataRequired('Введите название')],render_kw={'class': 'form-control'})
    tool_id=SelectField(u'Tool', coerce=int)
    type_id=SelectField('Тип', choices=ANN_TYPE, validators=[DataRequired('Нужно выбрать вы хотите сдать или взять в аренду')], render_kw={'class': 'form-control'})
    text=TextAreaField('Детали объявления', validators=[DataRequired('Добавьте деталей, пожалуйста')], render_kw={'class': 'form-control'})
    price=DecimalField('Цена за день', validators=[NumberRange(min=0, message='Укажите стоимость не менее 0')], render_kw={'class': 'form-control'})
    submit=SubmitField('Создать', render_kw={'class': 'btn btn-primary'})
=======
    remember=BooleanField('Запомнить', default=False, render_kw={"class":"form_check_input"})
    submit=SubmitField('Зайти')
>>>>>>> 5fde939d75b6ce04ffd2273854d35dc0a25b6a6f
