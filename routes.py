from unicodedata import category

from app import app
from flask import render_template,request,redirect,url_for,session,flash
import users,events,participants,comments

@app.route("/")
def index():
    user = users.user_id()
    public_events = events.show_all_public_events()
    private_events = events.show_all_private_events(user)
    invited_events = events.show_all_invited_events(user)


    return render_template('home.html',p_events=public_events, private_events=private_events,invited_events=invited_events)

@app.route("/register",methods=["GET","POST"])
def register_form():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
    if users.register(username,password):
        flash("Your account has been created ",category='info')
        return redirect("/")
    else:
         flash("The username is taken! ",category='warning')
         return render_template('register.html')

@app.route("/login",methods=["GET","POST"])
def login_form():
    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if users.login(username,password):
        flash("Successfully logged in",category='info')
        return redirect("/")
    
    else:
        flash("Wrong credentials",category="warning")
        return render_template("login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/my_events", methods=["GET","POST"])
@app.route('/my_events/<action>/<event_id>', methods=['GET', 'POST'])
def my_events(action = None, event_id=None):

    if request.method == "POST":
        if action=="delete":
            participants.delete_with_event_id(event_id)
            comments.delete_with_event_id(event_id)
            events.delete_event(event_id)
            return redirect("/my_events")
        
        if action=="modify":
            event_name = request.form["new_event_name"]
            event_description = request.form["new_event_desc"]
            event_privacy = request.form["new_privacy"]
            event_date = request.form["new_date"]
            event_id = event_id
            events.update_event(event_name,event_description,event_privacy,event_date,event_id)
            return redirect("/my_events")
        
        if action =="clear_comments":
            comments.delete_with_event_id(event_id)
            return redirect("/my_events")


    if request.method == "GET":
        my_events = events.show_user_events(users.user_id())
        return render_template("my_events.html",my_events = my_events)


@app.route("/create_event",methods=["GET","POST"])
def create_event():
    if request.method == "GET":
        return render_template("create_event.html")
    if request.method == "POST":
        event_name = request.form["event_name"]
        event_description = request.form["event_desc"]
        event_privacy = request.form["privacy"]
        event_date = request.form["date"]
        event_timeframe = request.form["time"]
        user_id = users.user_id()
        
        if events.create_event(event_name, event_description,event_privacy,event_date,event_timeframe,user_id):
            flash("You have successfully created a event!",category="info")
            return redirect("/")
        else:
            flash("Please check the input and try again!",category="warning")
            return redirect("/create_event")


@app.route("/event/<int:id>",methods=["GET","POST"])
@app.route('/event/<int:id>/<action>', methods=['GET', 'POST'])
def event(action=None,id=None):
    event = events.get_event(id)
    author = events.get_event_author(id)[0][0]
    event_participant = users.user_id()
    event_id = id

    get_participants = participants.get_participants(users.user_id(),id)
    get_comments = comments.show_events_comments(id)
    if request.method == "GET":
        return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)
    
    if request.method == "POST":
        if action == "join":            
            if participants.is_user_in_event(event_participant,event_id):
                flash("You have already joined this event!",category="warning")
                return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)

            participants.add_user_to_event(event_participant,event_id)
            flash("You have succefully joined the event!",category="info")
            get_participants = participants.get_participants(users.user_id(),event_id=id)

            return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)

        if action == "comment":
            content = request.form["content"]
            if users.user_id() == 0:
                flash("You need to login to leave a comment! ",category="warning")
                return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)

            
            comments.add_comment(content,event_participant, event_id)
            get_comments = comments.show_events_comments(id)
            
            return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)

@app.route("/users/<int:id>",methods=["GET","POST"])
def search_users(id = None):
    if request.method == "GET":
        return render_template("search_users.html",event_id=id)
    
    if request.method == "POST":
        searched_user = users.search_users(request.form["query"])[0][0]
        uid = users.get_user_id_by_username(searched_user)[0][0]
        
        if searched_user:
            invite_user = users.invite_user_to_event(uid,id)
            if invite_user:
                flash(f"You have successfully invited user {searched_user}",category="info")
            else:
                flash(f"User {searched_user} has already been invited !",category="warning")

        
        return render_template("search_users.html",event_id=id)