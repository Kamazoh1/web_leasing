from flask import Flask, render_template
from webapp.model import db, User, Announcement, Tool
from flask_sqlalchemy import SQLAlchemy
from webapp.forms import RegistrationForm, LoginForm



def create_app():

    app=Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)

    @app.route('/')
    def mainpage ():
        #message=test_db()
        return render_template('main.html')

    @app.route('/registration')
    def user_registration():
        pass

    @app.route('/login')
    def user_login():
        user_login_form=LoginForm()
        return render_template('Login.html', form=user_login_form)


    return app


def test_db ():
    user_test=User(name='Vasya', surname='Ivanov', email='b@b.ru', login='VIb', password='password')
    print (user_test)
    db.session.add(user_test)
    try:
        db.session.commit()
    except:
        return 'Пользователь с такими логином или почтой уже есть'
    return ('Проверьте, прошла ли запись в БД')
    

if __name__=='__main__':
    test_db()

