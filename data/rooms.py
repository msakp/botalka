import sqlalchemy
import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Room(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    timer = sqlalchemy.Column(sqlalchemy.Integer, default=60)

    lobby_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lobbies.id"))
    lobby = orm.relationship("Lobby")

    def __repr__(self):
        return "<Room> {}".format(self.name)
