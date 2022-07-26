from db import db
from flask import session
import users


def create_event(name,desc,privacy,date,timeframe,user_id):
    if privacy == "1":
        privacy = True
    elif privacy == "0":
        privacy = False
    else:
        privacy = "notset"

    if name != "" and privacy != "notset" and date != "" and timeframe != "":
        sql = "INSERT INTO events (event_name,event_description,event_date,event_time,ispublic,user_id) VALUES (:event_name,:event_description,:event_date,:event_time,:ispublic,:user_id)"
        db.session.execute(sql,{"event_name":name,"event_description":desc,"event_date":date,"event_time":timeframe,"ispublic":privacy,"user_id":int(user_id)})
        db.session.commit()
        return True
    return False

def show_all_public_events():
    sql = "SELECT * FROM events WHERE ispublic = True"
    result = db.session.execute(sql)
    return result.fetchall()

def show_all_private_events(user_id):
    sql = "SELECT * FROM events WHERE ispublic = False AND user_id=:user_id  "
    result = db.session.execute(sql,{"user_id":user_id})
    events = result.fetchall()
    return events

def show_all_invited_events(user_id):
    sql = "SELECT * FROM events E, invited I WHERE I.user_id=:user_id AND E.event_id=I.event_id AND NOT EXISTS (SELECT * FROM participant P WHERE P.user_id=I.user_id AND P.event_id=I.event_id)"
    
    
    result = db.session.execute(sql,{"user_id":user_id})
    events = result.fetchall()
    print(events)
    
    return events

def show_user_events(id):
    sql = "SELECT * FROM events WHERE user_id=:id"
    result = db.session.execute(sql,{"id":id})
    events = result.fetchall()
    return events

def get_event(id):
    sql = "SELECT * FROM events WHERE event_id=:id"
    result = db.session.execute(sql,{"id":id})
    events = result.fetchall()
    return events

def get_event_author(id):
    sql = "SELECT user_id FROM events WHERE event_id=:id"
    result = db.session.execute(sql,{"id":id})
    user_id = result.fetchall()[0][0]

    author = users.get_username(user_id)
    return author

def delete_event(event_id):
    sql = "DELETE FROM events WHERE event_id=:event_id"
    db.session.execute(sql,{"event_id":event_id})
    db.session.commit()
    return True


def update_event(name,desc,privacy,date,id):
    if name != "":
        sql = "UPDATE events SET event_name=:name WHERE event_id=:id "
        db.session.execute(sql,{"name":name, "id":id})
        db.session.commit()
    if desc != "":
        sql = "UPDATE events SET event_description=:desc WHERE event_id=:id "
        db.session.execute(sql,{"desc":desc, "id":id})
        db.session.commit()
    if privacy != "":
        if privacy == "1":
            privacy = True
        elif privacy == "0":
            privacy = False

        sql = "UPDATE events SET ispublic=:privacy WHERE event_id=:id "
        db.session.execute(sql,{"privacy":privacy, "id":id})
        db.session.commit()
    
    if date != "":
        sql = "UPDATE events SET event_date=:date WHERE event_id=:id "
        db.session.execute(sql,{"date":date, "id":id})
        db.session.commit()
