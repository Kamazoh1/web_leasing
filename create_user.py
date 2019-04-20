from getpass import getpass
import sys
from webapp.model import db, User
from webapp import create_app

app=create_app()

with app.app_context():
 #   new_user.email=input ('Введите email:')
 #   input ('Введите логин:')
 #   getpass ('Введите пароль:')
    new_user=User(name='Masha', surname='Petrova', email='a@b.ru', gender='Female', role='User')
    new_user.set_password('Masha')
    print (new_user)
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        print (str(e))
        print ('Запись не прошла')
        sys.exit(0)
    print ('Проверьте, прошла ли запись в БД')





