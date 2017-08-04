import bcrypt
import datetime
import flask
from flask_login import UserMixin
import sqlalchemy

from zappa_boilerplate.database import Base


class User(Base, UserMixin):

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(80), unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(80), unique=True, nullable=False)

    password = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)  # the hashed password
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    @staticmethod
    def create(session, username, email, password):
        user = User(username, email, password)
        session.add(user)
        session.flush()
        return user

    @classmethod
    def get_by_id(cls, session, user_id):
        if any(
            (isinstance(user_id, str) and user_id.isdigit(),
             isinstance(user_id, (int, float))),
        ):
            return session.query(cls).filter(cls.id == user_id).first()
        return None

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt(flask.current_app.config['BCRYPT_LOG_ROUNDS'])).decode('utf-8')

    def check_password(self, value):
        return bcrypt.checkpw(value.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
