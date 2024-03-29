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

def get_participants(user_id,event_id):
    sql = "SELECT user_id FROM participant WHERE event_id=:event_id"
    result = db.session.execute(sql, { "event_id":event_id} )
    matches = result.fetchall()
    user_ids = []

    for i in matches:
        user_ids.append(users.get_username(i[0])[0][0])
    return user_ids

def delete_with_event_id(event_id):
    try:
        sql = "DELETE FROM participant WHERE event_id=:event_id"
        db.session.execute(sql, { "event_id":event_id} )
        return True
    except:
        return False

def cancel_attendance(user_id,event_id):
    sql = "DELETE FROM participant WHERE event_id=:event_id AND user_id=:user_id"
    db.session.execute(sql, { "event_id":event_id,"user_id":user_id} )
    db.session.commit()

    sql = "DELETE FROM invited WHERE event_id=:event_id AND user_id=:user_id"
    db.session.execute(sql, { "event_id":event_id,"user_id":user_id} )
    db.session.commit()

def get_events_from_participant(user_id):
    sql = "SELECT * FROM events E, participant P WHERE P.user_id=:user_id AND P.event_id=E.event_id ORDER BY E.event_date "
    result = db.session.execute(sql, { "user_id":user_id} )
    matches = result.fetchall()
    return matches

def order_by_max_participants():
    sql = """
    SELECT E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    FROM events E
    LEFT OUTER JOIN participant P ON (E.event_id = P.event_id AND E.ispublic=True) WHERE
    E.ispublic = True
    GROUP BY E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    ORDER BY COUNT(*) DESC
    """

    result = db.session.execute(sql)
    matches = result.fetchall()
    return matches

def order_by_max_participants_private(user_id):
    sql = """
    SELECT E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    FROM events E
    LEFT OUTER JOIN participant P ON (E.event_id = P.event_id AND E.ispublic=False AND P.user_id=:user_id) 
    WHERE E.ispublic = False AND P.user_id=:user_id
    GROUP BY E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    ORDER BY COUNT(*) DESC
    """

    result = db.session.execute(sql,{"user_id":user_id})
    matches = result.fetchall()
    return matches

