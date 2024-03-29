from db import db
from flask import session
import users,participants,comments
from datetime import date
from datetime import datetime


def create_event(name,desc,privacy,date,timeframe,user_id):
    if privacy == "1":
        privacy = True
    elif privacy == "0":
        privacy = False
    else:
        privacy = "notset"

    if name != "" and privacy != "notset" and date != "" and timeframe != "":
        try:
            sql = "INSERT INTO events (event_name,event_description,event_date,event_time,ispublic,user_id) VALUES (:event_name,:event_description,:event_date,:event_time,:ispublic,:user_id)"
            db.session.execute(sql,{"event_name":name,"event_description":desc,"event_date":date,"event_time":timeframe,"ispublic":privacy,"user_id":int(user_id)})
            db.session.commit()
            return True
        except:
            return False
    return False

def show_all_public_events():
    sql = "SELECT * FROM events WHERE ispublic = True ORDER BY event_date"
    result = db.session.execute(sql)
    return result.fetchall()

def show_all_private_events_with_id(user_id):
    sql = "SELECT * FROM events WHERE ispublic = False AND user_id=:user_id ORDER BY event_date "
    result = db.session.execute(sql,{"user_id":user_id})
    events = result.fetchall()
    return events

def show_all_invited_events_with_id(user_id):

    sql = "SELECT * FROM events JOIN invited ON invited.user_id=:user_id AND events.event_id=invited.event_id AND NOT EXISTS (SELECT * FROM participant P WHERE P.user_id=invited.user_id AND P.event_id=invited.event_id) ORDER BY events.event_date"
    result = db.session.execute(sql,{"user_id":user_id})
    events = result.fetchall()    
    return events

def get_all_events():
    sql = "SELECT * FROM events"
    result = db.session.execute(sql)
    events = result.fetchall()
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

def get_event_name(id):
    sql = "SELECT event_name FROM events WHERE event_id=:id"
    result = db.session.execute(sql,{"id":id})
    event_name = result.fetchall()[0][0]
    return event_name


def delete_event(event_id):
    sql = "DELETE FROM events WHERE event_id=:event_id"
    db.session.execute(sql,{"event_id":event_id})
    db.session.commit()
    return True

def is_old_event(given_date):
    print(given_date)
    event_date = datetime.strptime(given_date,'%Y-%m-%d').date()
    print(event_date)
    todays_date = date.today()

    if (event_date > todays_date) == False:
        return True
    else:
        return False

def clear_old_events():
    events = get_all_events()
    today_date = date.today()
    
    for event in events:
        event_date = event[3]
        if (event_date > today_date) == False:
            event_id = event[0]
            participants.delete_with_event_id(event_id)
            comments.delete_with_event_id(event_id)
            delete_event(event_id)

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
