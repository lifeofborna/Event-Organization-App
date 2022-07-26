from db import db
from flask import session
import users


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

