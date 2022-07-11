from db import db
from flask import session


#give all parameters > add db
def create_event(name,desc,privacy,date,timeframe,user_id):
    print(user_id, "XDDDDDDDDDDDd")
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
def show_events():
    return 1

#delete all events
def delete_event():
    return 3
    
#show events where id = session id
def show_autors_events():
    return 4