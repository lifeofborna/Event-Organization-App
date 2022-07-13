from db import db
from flask import session
import users,events



def add_user_to_event(user_id, event_id):
    sql = "INSERT into participant (user_id,event_id) VALUES (:user_id,:event_id)"
    db.session.execute(sql, { "user_id":user_id, "event_id":event_id} )
    db.session.commit()

def is_user_in_event(user_id,event_id):
    sql = "SELECT * FROM participant WHERE user_id=:user_id AND event_id=:event_id"
    result = db.session.execute(sql, { "user_id":user_id, "event_id":event_id} )
    users = result.fetchall()

    if users: return True

    return False
    