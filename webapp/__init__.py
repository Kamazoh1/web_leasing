from flask import Flask, render_template, flash, redirect, url_for
from webapp.model import db, User, Announcement, Tool, GENDER
from flask_sqlalchemy import SQLAlchemy
from webapp.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
#for password encription
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from datetime import datetime
#for managing login process

def create_app():

    app=Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager=LoginManager() #экземпляр LoginManager
    login_manager.init_app (app) #init
    login_manager.login_view='user_login' #Как будет названа функция, которая будет заниматься логином пользователя


    @login_manager.user_loader
    def load_user (user_id):
        return User.query.get(user_id) #получение пользователя по его idю Возврашщает объект User


    @app.route('/')
    def mainpage ():
        #message=test_db()
        return render_template('main.html')


    @app.route('/registration') #пока тестирование БД и создание в ней одного пользователя
    def user_registration ():
    #    if current_user.is_authenticated:
     #       flash('Да Вы же уже представились, мы Вас узнали! Зачем же еще раз регистрироваться?')
      #      return redirect(url_for('mainpage'))
        user_reg_form=RegistrationForm()
        return render_template('registration.html', form=user_reg_form)

    @app.route('/registration_process', methods=['POST'])
    def process_registration():
        r_form=RegistrationForm()
        if r_form.validate_on_submit():
            if User.query.filter(User.email==r_form.email.data).count():
                flash('Пользователь с такой эл.почтой уже есть')
                return redirect(url_for('user_registration'))
            #Здесь добавить отслеживание ошибок displaying error https://wtforms.readthedocs.io/en/stable/crash_course.html
            new_user=User(name=r_form.name.data, surname=r_form.surname.data, email=r_form.email.data, gender=r_form.gender.data, role='U')
            new_user.set_password(r_form.password.data)
            new_user.gender=r_form.gender.data
            #flash ('До записи в БД все нормально')
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('Приятно познакомиться! Мы Вас запомнили.')
            except Exception as e:
                flash(str(e))
                flash('Что-то пошло не так с новым пользователем...')
                return redirect(url_for('user_registration'))
            return redirect(url_for('user_login'))
        flash('Заполните все поля формы!')
        return redirect(url_for('user_registration'))

<<<<<<< HEAD
=======
    @app.route('/addAnnouncement')
    @login_required
    def add_announcement():
        ad_an_form = AddAnnouncementForm()
        return render_template('addAnnouncement.html', form=ad_an_form)
    
    @app.route('/announcement_registration', methods=['GET','POST'])
    @login_required
    def announcement_registration():
        a_form=AddAnnouncementForm()
        tool_ = a_form.tool_id.data
        if a_form.validate_on_submit():
            if not Announcement.query.filter(Announcement.user_id==current_user.id, Announcement.tool_id==tool_.id).count():
            #if Announcement.query.filter(Announcement.user_id==current_user.id).count():

                new_announcement=Announcement(user_id=current_user.id,
                                            type_id=a_form.type_id.data, 
                                            head=a_form.head.data, 
                                            text=a_form.text.data,
                                            tool_id=tool_.id,
                                            pub_datetime=datetime.now(),
                                            price=a_form.price.data,
                                            address=a_form.address.data)
                db.session.add(new_announcement)
            try:
                db.session.commit()
            except Exception as e:
                flash(str(e))
            flash('Ваше объявление успешно зарегистрировано.')
            return redirect(url_for('mainpage'))
        flash('К сожалению, нельзя иметь два объявления на один товар одновременно')
        return redirect(url_for('addAnnouncement'))

>>>>>>> e35cc83187658b4134fe942009cf58cc5ae17176
    @app.route('/login')
    def user_login():
        if current_user.is_authenticated:
            flash('Да Вы же уже представились, мы Вас узнали!')
            return redirect(url_for('mainpage'))
        user_login_form=LoginForm()
        return render_template('login.html', form=user_login_form)


    @app.route('/process_login', methods=['POST'])
    def process_login():
        l_form=LoginForm() #создаем экземпляр формы
        if l_form.validate_on_submit(): #делаем проверку формы: если пришли данные формы, и пришли без ошибок, в том числе без отсутствия необходимых данных
            user=User.query.filter(User.email==l_form.email.data).first()
            if user and user.check_password(l_form.password.data): #если пользователь существует и пароль верный
                login_user(user, remember=l_form.remember.data) #залогинить пользователя. здесь происходит внутренняя магия flask_login'а
                flash('А, так это ты! Заходи-заходи!')
                return redirect(url_for('mainpage'))
            flash('То ли логина такого нет, то ли пароль у него другой. /n Попробуйте еще раз!')
            return redirect(url_for('user_login'))
        flash('Заполните все поля формы!')
        return redirect(url_for('user_login'))

    @app.route('/logout')
    def user_logout():
        logout_user()
        flash('Теперь я снова тебя не узнаю...')
        return redirect (url_for('mainpage'))

    @app.route('/admin')
    @login_required  #это называется "декоратор"
    # если пользователь не аутентифицирован, то будет выдана ошибка, по умолчанию перебрасывает на login_view
    def admin_room():
        if current_user.is_admin: #current_user - from flask_login
            return 'Да, ты Админ! Ты такой Админ!!!'
        else:
            return 'А тебе сюда низзя!'
            #redirect(url_for('user_login'))

    @app.route('/announcements')
    @login_required
    def show_announcements():
        try:
            ann_set=Announcement.query.all()
            print('из БД скачалось')
            for i in ann_set:
                i.pub_datetime= datetime.strptime(i.pub_datetime, '%d-%m-%y')
            #print (str(ann_set[0]))
            return render_template('announcement_list.html', ann_set=ann_set)
        except Exception as e:
            print(str(e))
            flash(str(e))
            return str(e)


    @app.route('/test_db')
    def test_01():
        return test_db()



    return app


def test_db ():
    user_test=User(name='Vasya', surname='Ivanov', email='b@b.ru', password='password', gender='Male', role='User')
    print (user_test)
    db.session.add(user_test)
    try:
        db.session.commit()
    except Exception as e:
        return str(e)
    return ('Проверьте, прошла ли запись в БД')
    

if __name__=='__main__':
    test_db()

