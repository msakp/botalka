import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Lobby(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lobbies'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    user = orm.relationship("User")

    def __repr__(self):
        return "<Lobby> {}".format(self.id)
