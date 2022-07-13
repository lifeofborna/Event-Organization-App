from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def login(username,password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    search_for_user = db.session.execute(sql, {"username":username})
    user = search_for_user.fetchone()

    if not user:
        return False
    else:
        if check_password_hash(user.password,password):
            session["user_id"] = user.user_id
            return True
        else:
            return False



def register(username,password):
    hashed_password = generate_password_hash(password)
    isadmin = False
    
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

def get_username(id):
    sql = "SELECT username FROM users WHERE user_id=:id"
    result = db.session.execute(sql,{"id":id})
    author = result.fetchall()
    return author