from getpass import getpass
import sys
from webapp.model import db, User
from webapp import create_app

app=create_app()

with app.app_context():
    print('Ну не доделано оно, не доделано!')
    new_user=User()
    new_user.email=input ('Введите email:')
    input ('Введите логин:')
    getpass ('Введите пароль:')


