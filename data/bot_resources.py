from flask_restful import Resource, reqparse
from flask import abort, jsonify
from . import db_session
from data.rooms import Room
from data.lobbies import Lobby

def abort_if_room_not_found(room_name):
    session = db_session.create_session()
    room = session.query(Room).get(room_name)
    if not room:
        abort(404, message=f"Room {room_name} not found")


parser = reqparse.RequestParser()
parser.add_argument("name", required=True, location="form")
parser.add_argument("timer", required=True, type=int, location="form")


class LobbyResource(Resource):
    def get(self, lobby_id):
        db_sess = db_session.create_session()
        rooms = db_sess.query(Room).filter(Room.lobby_id == lobby_id).all()
        db_sess.close()
        return jsonify({"rooms": [room.to_dict(only=("name", "timer")) for room in rooms]})
    
    def post(self, lobby_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        current_lobby = db_sess.query(Lobby).filter(Lobby.id == lobby_id).first()
        room = Room(name=args["name"], timer=args["timer"], lobby=current_lobby)
        db_sess.add(room)
        db_sess.commit()
        info =  room.to_dict(only=("name", "timer"))
        db_sess.close()
        return jsonify({"room": info})

