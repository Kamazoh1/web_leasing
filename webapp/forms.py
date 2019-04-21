from flask_wtf import FlaskForm
#https://flask-wtf.readthedocs.io/ 
#https://www.tutorialspoint.com/flask/flask_wtf.htm - с перечислением типов
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField 
#импортируем типы полей 
from wtforms.validators import DataRequired, Email
#validator - класс, который помогает избежать ручных проверок
#DataRequired - проверяет, что пользователь действительно вбил данные



class RegistrationForm (FlaskForm): #наследуем форму от FlaskForm
    name=StringField('Имя пользователя', validators=[DataRequired('Введите имя')])
    surname=StringField('Фамилия пользователя', validators=[DataRequired('Введите фамилию')])
    password=PasswordField('Пароль', validators=[DataRequired('Какой вы хотите себе пароль?')])
    email=StringField('Адрес эл.почты', validators=[DataRequired('Какой у вас адрес электронной почты?'), Email('Тут нужен адрес электронной почты')])
    gender=RadioField('Пол', choices=(
    ('M', 'Мужской'),
    ('F', 'Женский'),
    ('O', 'Другой')), validators=[DataRequired('Какого вы пола?')])
    submit=SubmitField('Зарегистрироваться')


class LoginForm (FlaskForm):
    email=StringField('Ваш адрес электронной почты:', validators=[DataRequired('Укажите Ваш адрес эл.почты')])
    password=PasswordField('Пароль:', validators=[DataRequired('Введите Ваш пароль')])
    remember=BooleanField('Запомнить', default=True, render_kw={"class":"form_check_input"})
    submit=SubmitField('Зайти')