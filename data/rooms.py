import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Room(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
