from db import db
from flask import session
import users


#give all parameters > add db
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
    return 2

#return all events
def show_all_public_events():
    
    sql = "SELECT * FROM events WHERE ispublic = True"
    result = db.session.execute(sql)
    return result.fetchall()


def show_user_events(id):
    sql = "SELECT * FROM events WHERE user_id=:id"
    result = db.session.execute(sql,{"id":id})
    events = result.fetchall()
    return events

#delete all events
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





def delete_event():
    return 3
