from flask import Flask, session
from flask import render_template, redirect, request, make_response, jsonify
from flask_login import (LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user)
from data import db_session
from data.users import User
from data.lobbies import Lobby
from data.rooms import Room

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.roomform import RoomForm

from flask_restful import reqparse, abort, Api, Resource
from data.bot_resources import LobbyResource


app = Flask(__name__)
app.config["SECRET_KEY"] = "arstoienqwfp;yulfqwpoiesvk"
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
api.add_resource(LobbyResource, "/api/lobby")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", title="botalka")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
        )
        user.set_password(form.password.data)
        user.lobby_id = user.create_lobby(db_sess)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/new_room", methods=["GET", "POST"])
@login_required
def new_room():
    form = RoomForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        room = Room(name=form.name.data)
        db_sess.add(room)
        db_sess.commit()
        current_user.lobby.rooms += ";{}".format(room.id)
        db_sess.add(current_user.lobby)
        db_sess.commit()
        db_sess.close()
        return redirect("/lobby")
        
    return render_template("roomform.html", form=form, title="Новая комната")


@app.route("/lobby")
def loddy():
    if current_user.is_authenticated:
        return render_template("lobby.html", title="Лобби")
    return redirect("/login")


def main():
    db_session.global_init("db/botalka.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
