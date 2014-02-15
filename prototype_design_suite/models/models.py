from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
import datetime
import random
import string


from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    Boolean,
    String,
    ForeignKey,
    )

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class UserData(Base):
    __tablename__='userdata'
    id = Column(Integer, primary_key=True,)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    user_reg_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_last_logged_on = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_email(cls, email):
        return DBSession.query(UserData).filter(UserData.user_email == email).first()

    def verify_password(self, password):
        return pwd_context.verify(password, self.user_password)

    @classmethod
    def addAccount(cls, new_user_email, new_user_password, new_user_name):
        hash = pwd_context.encrypt(new_user_password)
        user = UserData(user_email=new_user_email, user_password=hash, user_name=new_user_name)
        DBSession.add(user)

    @classmethod
    def get_user(cls, email):
        user = DBSession.query(UserData).filter(UserData.user_email == email).first()
        if(user != None):
            return (True, user)
        else:
            return (False, None)

    @classmethod
    def logged_in(cls, email):
        user = DBSession.query(UserData).filter(UserData.email == email).first()
        user.user_last_logged_on = datetime.datetime.utcnow

    @classmethod
    def display_name_check(cls, email):
        user = DBSession.query(UserData).filter(UserData.email == email).first()
        if user.user_name_public:
            return True
        else:
            return False





#####################################
#Table for password recovery process#
#####################################

class PasswordReset(Base):
    __tablename__='password_change_requests'
    id = Column(Integer, primary_key=True,)
    email = Column(String, nullable=False)
    key = Column(String, default = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(50)))
    requested = Column(DateTime, default=datetime.datetime.now)


    @classmethod
    def logRequest(cls, old_email):
        data = PasswordReset(email=old_email)
        DBSession.add(data)
        #now get the user by email
        user = DBSession.query(PasswordReset).filter(PasswordReset.email == old_email).first()
        #get the string for the url
        return user.key

    @classmethod
    def verify(cls, key):
        user = DBSession.query(PasswordReset).filter(PasswordReset.key == key).first()
        if user is not None:
            return True
        else:
            return False

    @classmethod
    def passwordReset(cls, key, password):
        data = DBSession.query(PasswordReset).filter(PasswordReset.key == key).first()
        if data is not None:
            user = DBSession.query(UserData).filter(UserData.email == data.email).first()
            hash = pwd_context.encrypt(password)
            user.password = hash
            #delete
            DBSession.query(PasswordReset).filter(PasswordReset.key == key).delete()
            return True
        else:
            return False





