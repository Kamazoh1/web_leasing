from flask_sqlalchemy import SQLAlchemy
#http://flask-sqlalchemy.pocoo.org/2.3/
#
import sqlalchemy.types as types
#from flask_sqlalchemy import types

from flask_login import UserMixin
#UserMixin for working with authentification and login processes

from werkzeug.security import generate_password_hash, check_password_hash
#for password encription




GENDER=(
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'))

ANN_TYPE=(
    ('L', 'Lease'),
    ('G', 'Get'))
    
ROLE=(
    ('A', 'Admin'),
    ('U', 'User'))


class ChoiceType (types.TypeDecorator):

    impl=types.String

    def __init__ (self, choices, **kw):
        self.choices=dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v==value][0]

    def process_result_value(self, value, dialect):
        return self.choices.get(value, value)



#--------------------------------------------------------------


db=SQLAlchemy()


class User (db.Model, UserMixin):
    __tablename__='User'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, unique=False, nullable=False)
    surname=db.Column(db.String, unique=False, nullable=False)
    email=db.Column(db.String, index=True, unique=True, nullable=False)
    password=db.Column(db.String, unique=False, nullable=False)
    rating=db.Column(db.Float, unique=False, nullable=True)
    phone=db.Column(db.String, unique=True, nullable=True)
    details=db.Column(db.String, unique=False, nullable=True)
    gender=db.Column(ChoiceType(choices=GENDER), unique=False, nullable=True)
    active=db.Column(db.Boolean, index=True, unique=False, nullable=False, default=True)
    role=db.Column(ChoiceType(choices=ROLE), index=True, unique=False, nullable=False)
    address=db.Column(db.String, index=True, unique=False, nullable=True)
    #ForeignKeys
    rel_ann=db.relationship('Announcement', back_populates='rel_user_id')

    def set_password (self, password):
        self.password=generate_password_hash (password)

    def check_password (self, password):
        return check_password_hash (self.password, password)

    def __repr__(self):
        return '<User: {} {}, email {}>'.format (self.name, self.surname, self.email)

    @property
    def is_admin(self):
        return self.role=='Admin'


class Announcement (db.Model):
    __tablename__='Announcement'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('User.id'), index=True, unique=False, nullable=False)
    type_id=db.Column(ChoiceType(choices=ANN_TYPE), index=True, unique=False, nullable=False)
    head=db.Column(db.String, unique=False, nullable=False)
    text=db.Column(db.Text, unique=False, nullable=False)
    tool_id=db.Column(db.Integer, db.ForeignKey('Tool.id'), index=True, unique=False, nullable=False)
    pub_datetime=db.Column(db.DateTime, unique=False, nullable=False)
    arch_datetime=db.Column(db.DateTime, unique=False, nullable=True)
    price=db.Column(db.Float, unique=False, nullable=False)
    address=db.Column(db.String, index=True, unique=False, nullable=False)
    #ForeignKeys
    rel_user_id=db.relationship('User', back_populates='rel_ann')
    rel_tool_id=db.relationship('Tool', back_populates='rel_ann')


    def __repr__(self):
        return '<Announcement: {} {}, head {}, user {}>'.format (self.id, self.type, self.head, self.user_id)


# Я решил, что все же нужна отдельная таблица иерархии. 
class Category(db.Model):
    __tablename__='Category'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, unique=True, nullable=False)
    description=db.Column(db.String, unique=True, nullable=True)
    parent_categoryid=db.Column(db.Integer, db.ForeignKey('Category.id'), index = True, unique=False, nullable=True)
    rel_tool_id=db.relationship('Tool', back_populates='rel_category_id')

    def __repr__(self):
        return '<Category: id{} name {} parentid {}'.format(self.id, self.name, self.parent_categoryid)



class Tool (db.Model):
    __tablename__='Tool'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, unique=True, nullable=False)
    description=db.Column(db.String, unique=True, nullable=True)
    #parent_id=db.Column(db.String, db.ForeignKey('Tool.id'), unique=False, nullable=False)
    # Нам по хорошему тут нужна картинка товара.
    #ForeignKeys
    categoryid = db.Column(db.Integer, db.ForeignKey('Category.id'), index=True, unique=False, nullable=False)
    rel_ann=db.relationship('Announcement', back_populates='rel_tool_id')
    rel_category_id=db.relationship('Category', back_populates='rel_tool_id')
    #parent_tool=db.relationship('Tool')

    def __repr__(self):
        return '<Tool: id {} name {} categoryid {}>'.format (self.id, self.name, self.rel_category_id)
        


"""
class Ann_comment (db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False, unique=False, nullable=False)
    ann_id=db.Column(db.Integer, db.ForeignKey('Announcement.id'), primary_key=False, unique=False, nullable=False)
    pub_datetime=db.Column(db.DateTime, primary_key=False, unique=False, nullable=False)
    text=db.Column(db.String, primary_key=False, unique=False, nullable=False)
    #либо valid, либо arch_datetime / del_datetime

    #ForeignKeys

    def __repr__(self):
        pass


class User_comment (db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    author_id=db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False, unique=False, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False, unique=False, nullable=False)
    pub_datetime=db.Column(db.DateTime, primary_key=False, unique=False, nullable=False)
    rating=db.Column(db.Integer, primary_key=False, unique=False, nullable=False) #может ли быть без рейтинга???
    #ForeignKeys

    
    def __repr__(self):
        pass


class Message (db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    from_id=db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False, unique=False, nullable=False)
    to_id=db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False, unique=False, nullable=False)
    datetime=db.Column(db.DateTime, primary_key=False, unique=False, nullable=False)
    theme=db.Column(db.String, primary_key=False, unique=False, nullable=False) #может ли быть без рейтинга???
    text=db.Column(db.Text, primary_key=False, unique=False, nullable=False)
    read=db.Column(db.Boolean, primary_key=False, unique=False, nullable=False)
    #ForeignKeys

    def __repr__(self):
        pass

"""
