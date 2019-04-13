from flask_sqlalchemy import SQLAlchemy
#http://flask-sqlalchemy.pocoo.org/2.3/
#

GENDER=(
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'))

ANN_TYPE=(
    ('L', 'Lease'),
    ('G', 'Get'))
    
ROLE=(
    ('A', 'Administrator'),
    ('U', 'User'))


class ChoiceType (types.TypeDecorator):

    impl=types.String

    def __init__ (self, choices, **kw):
        self.choices=dict(choices)
        super(ChoiceType, self).__init__(*kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v==value][0]

    def process_result_value(self, value, dialect):
        return self.choices.get(value, value)



#--------------------------------------------------------------


db=SQLAlchemy()


class User (db.Model):
    __tablename__='User'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, unique=False, nullable=False)
    surname=db.Column(db.String, unique=False, nullable=False)
    email=db.Column(db.String, index=True, unique=True, nullable=False)
    login=db.Column(db.String, index=True, unique=True, nullable=False)
    password=db.Column(db.String, unique=False, nullable=False)
    rating=db.Column(db.Float, unique=False, nullable=True)
    phone=db.Column(db.String, unique=True, nullable=True)
    details=db.Column(db.String, unique=False, nullable=True)
    gender=db.Column(ChoiceType, choices=GENDER, unique=False, nullable=False)
    active=db.Column(db.Boolean, index=True, unique=False, nullable=False, default=True)
    role=db.Column(ChoiceType, choices=ROLE, Index=True, unique=False, nullable=False)
    #ForeignKeys
    rel_ann=db.relationship('Announcement', back_populates='rel_user_id')

    def __repr__(self):
        return '<User: {} {}, login {}, email {}>'.format (self.name, self.surname, self.login, self.email)

"""
class Ann_type (db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, primary_key=False, unique=True, nullable=False)
    description=db.Column(db.String, primary_key=False, unique=True, nullable=False)
    #ForeignKeys
    announcements = db.relationship('Announcement')

    def __repr__(self):
        pass
"""

class Announcement (db.Model):
    __tablename__='Announcement'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False, unique=False, nullable=False)
    type_id=db.Column(db.Enum, primary_key=False, unique=False, nullable=False)
    head=db.Column(db.String, primary_key=False, unique=False, nullable=False)
    text=db.Column(db.Text, primary_key=False, unique=False, nullable=False)
    tool_id=db.Column(db.Integer, db.ForeignKey('Tool.id'), primary_key=False, unique=False, nullable=False)
    #valid=db.Column(db.Boolean, primary_key=False, unique=False, nullable=False) #или ограничиться датой удаления?
    pub_datetime=db.Column(db.DateTime, primary_key=False, unique=False, nullable=False)
    arch_datetime=db.Column(db.DateTime, primary_key=False, unique=False, nullable=True)
    price=db.Column(db.Float, primary_key=False, unique=False, nullable=False)
    #ForeignKeys
    rel_user_id=db.relationship('User', back_populates='rel_ann')
    rel_tool_id=db.relationship('Tool', back_populates='rel_ann')


    def __repr__(self):
         return '<Announcement: {} {}, head {}, user {}>'.format (self.id, self.type, self.head, self.user_id)



class Tool (db.Model):
    __tablename__='Tool'
    id=db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, primary_key=False, unique=True, nullable=False)
    description=db.Column(db.String, primary_key=False, unique=True, nullable=True)
    parent_id=db.Column(db.String, db.ForeignKey('Tool.id'), primary_key=False, unique=False, nullable=False)
    #ForeignKeys
    rel_ann=db.relationship('Announcement', back_populates='rel_tool_id')
    #parent_tool=db.relationship('Tool')

    def __repr__(self):
        pass


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
