from flask_restful import Resource, reqparse
from flask import abort, jsonify
from flask_login import current_user
from . import db_session
from data.rooms import Room
from data.lobbies import Lobby


def abort_if_room_not_found(room_name):
    session = db_session.create_session()
    room = session.query(Room).get(room_name)
    if not room:
        abort(404, message=f"Room {room_name} not found")


parser = reqparse.RequestParser()
parser.add_argument("name", required=True)


class LobbyResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        rooms = db_sess.query(Room).filter(Room.id.in_(current_user.lobby.rooms.split(';'))).all()
        
        return jsonify({"rooms": [room.to_dict(only=("name",)) for room in rooms]})
