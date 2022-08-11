from db import db
from flask import session,request,abort
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
from app import app


def login(username,password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    search_for_user = db.session.execute(sql, {"username":username})
    user = search_for_user.fetchone()

    if not user:
        return False
    else:
        if check_password_hash(user.password,password):
            session["user_id"] = user.user_id
            session["csrf_token"] = token_hex(16)
            session["is_admin"] = check_if_admin()
            return True
        else:
            return False

def register(username,password):
    hashed_password = generate_password_hash(password)
    if username == "admin":
        isadmin = True
    else: isadmin = False
    
    try:
        sql = "INSERT into users (username,password,isadmin) VALUES (:username,:password,:isadmin)"

        db.session.execute(sql, { "username":username, "password":hashed_password, "isadmin":f"{isadmin}"} )
        db.session.commit()
    except:
        return False
    return login(username,password)

def logout():
    del session["user_id"]

def user_id():
    return session.get("user_id",0)

def check_if_admin():
    uid = user_id()
    sql = "SELECT * FROM users WHERE user_id=:uid AND isadmin=TRUE"
    result = db.session.execute(sql,{"uid":uid})
    is_admin = result.fetchall()
    if is_admin:
        return True
    else:
        return False

def get_username(id):
    sql = "SELECT username FROM users WHERE user_id=:id"
    result = db.session.execute(sql,{"id":id})
    author = result.fetchall()
    return author

def get_user_id_by_username(username):
    sql = "SELECT user_id FROM users WHERE username=:username"
    result = db.session.execute(sql,{"username":username})
    author = result.fetchall()
    return author

def search_users(query):
    sql = "SELECT username FROM users WHERE username =:query"
    result = db.session.execute(sql,{"query":query})
    users = result.fetchall()
    return users


def user_invited(user_id,event_id):
    sql = "SELECT * FROM invited WHERE user_id=:user_id AND event_id=:event_id"
    result = db.session.execute(sql,{"user_id":user_id, "event_id":event_id})
    author = result.fetchall()

    if author:
        return True
    return False

def invite_user_to_event(user_id, event_id):
    if user_invited(user_id,event_id):
        return False

    if user_id and event_id:
        sql = "INSERT into invited (user_id,event_id) VALUES (:user_id,:event_id)"
        db.session.execute(sql, { "user_id":user_id, "event_id":event_id})
        db.session.commit()
        return True

    return False



def authorization_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)