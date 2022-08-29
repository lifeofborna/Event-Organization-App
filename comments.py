from db import db
from flask import session


def add_comment(content,user_id,event_id):
    sql = "INSERT INTO comments (content, user_id, event_id, sent_at) VALUES (:content,:user_id,:event_id,NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id, "event_id":event_id})
    db.session.commit()

    return True

def show_events_comments(id):
    sql = "SELECT C.content,U.username,C.sent_at FROM comments C, users U WHERE C.user_id=U.user_id AND C.event_id=:id ORDER BY C.sent_at DESC LIMIT 5"
    result = db.session.execute(sql, { "id":id})
    all_results = result.fetchall()

    return all_results

def delete_with_event_id(event_id):
    sql = "DELETE FROM comments WHERE event_id=:event_id"
    db.session.execute(sql,{"event_id":event_id})
    db.session.commit()

def order_via_most_comments():

    sql = """
    SELECT E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    FROM events E
    LEFT OUTER JOIN comments C ON (E.event_id = C.event_id AND E.ispublic=True) 
    WHERE E.ispublic=True
    GROUP BY E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    ORDER BY COUNT(*) DESC """

    result = db.session.execute(sql)
    matches = result.fetchall()
    return matches

def order_via_most_comments_private(user_id):
    sql = """
    SELECT E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    FROM events E
    LEFT OUTER JOIN participant P ON (E.event_id = P.event_id AND E.ispublic=False AND P.user_id=:user_id) 
    LEFT OUTER JOIN comments C ON (E.event_id = C.event_id AND E.ispublic=False AND P.user_id=:user_id)
    WHERE E.ispublic=False AND p.user_id=:user_id
    GROUP BY E.event_id, E.event_name, E.event_description, E.event_date, E.event_time
    ORDER BY COUNT(*) DESC """

    result = db.session.execute(sql,{"user_id":user_id})
    matches = result.fetchall()

    return matches

