from unicodedata import category
from app import app
from flask import render_template,request,redirect,url_for,session,flash
import users,events,participants

@app.route("/")
def index():
    p_events = events.show_all_public_events()
    return render_template('home.html',p_events=p_events)

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
        flash("Wrong credentials")
        return render_template("login.html",category='warning')

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/my_events")
def my_events():
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
def event(id):
    event = events.get_event(id)
    author = events.get_event_author(id)[0][0]

    if request.method == "GET":
        return render_template("event.html",event=event,author=author)
    
    if request.method == "POST":
        event_participant = users.user_id()
        event_id = id

        if participants.is_user_in_event(event_participant,event_id):
            flash("You have already joined this event!",category="warning")
            return render_template("event.html",event=event,author=author)

        participants.add_user_to_event(event_participant,event_id)
        flash("You have succefully joined the event!",category="info")

        return render_template("event.html",event=event,author=author)
