from app import app
from flask import render_template,request,redirect,url_for,session,flash
import users,events,participants,comments

@app.route("/")
def index():
    events.clear_old_events()
    user = users.user_id()
    public_events = events.show_all_public_events()
    private_events = events.show_all_private_events_with_id(user)
    invited_events = events.show_all_invited_events_with_id(user)


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
    if check_authorization(auth_level="login") == False:
        return redirect("/login")
    
    elif check_authorization(auth_level="", action=action, event_id=event_id) == False:
        return redirect("/")

    if request.method == "POST":
        users.authorization_csrf()
        if action=="delete":
            participants.delete_with_event_id(event_id)
            comments.delete_with_event_id(event_id)
            events.delete_event(event_id)
            flash("You have successfully deleted the event!",category="info")
            return redirect("/my_events")
        
        if action=="modify":
            event_name = request.form["new_event_name"]
            event_description = request.form["new_event_desc"]
            event_privacy = request.form["new_privacy"]
            event_date = request.form["new_date"]
            event_id = event_id

            if len(event_name) > 30 or len(event_description) > 150:
                flash("Please use a valid input! max length for description is 150 characters and for title 30!",category="warning")
                return redirect("/my_events")
                
            events.update_event(event_name,event_description,event_privacy,event_date,event_id)
            flash("You have successfully modified the event!",category="info")
            return redirect("/my_events")
          
        if action =="clear_comments":
            flash("You have successfully cleared comments!",category="info")
            comments.delete_with_event_id(event_id)
            return redirect("/my_events")


    if request.method == "GET":
        my_events = events.show_user_events(users.user_id())
        return render_template("my_events.html",my_events = my_events)


@app.route("/create_event",methods=["GET","POST"])
def create_event():
    if check_authorization(auth_level="login") == False:
        return redirect("/login")

    if request.method == "GET":
        return render_template("create_event.html")
    if request.method == "POST":
        users.authorization_csrf()
        event_name = request.form["event_name"]
        event_description = request.form["event_desc"]
        event_privacy = request.form["privacy"]
        event_date = request.form["date"]
        event_timeframe = request.form["time"]
        user_id = users.user_id()
        
        if len(event_name) > 30 or len(event_description) > 150:
                flash("Please use a valid input! max length for description is 150 characters and for title 30!",category="warning")
                return redirect("/create_event")
        if events.create_event(event_name, event_description,event_privacy,event_date,event_timeframe,user_id):
            flash("You have successfully created a event!",category="info")
            return redirect("/")
        else:
            flash("Please check the input and try again!",category="warning")
            return redirect("/create_event")


@app.route("/event/<int:id>",methods=["GET","POST"])
@app.route('/event/<int:id>/<action>', methods=['GET', 'POST'])
def event(action=None,id=None):

    if check_authorization(auth_level="login") == False:
        return redirect("/login")

    event = events.get_event(id)
    author = events.get_event_author(id)[0][0]
    event_participant = users.user_id()
    event_id = id

    get_participants = participants.get_participants(users.user_id(),id)
    get_comments = comments.show_events_comments(id)
    if request.method == "GET":
        return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)
    
    if request.method == "POST":
        users.authorization_csrf()
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
            
            if len(content) > 250:
                flash("Max size for a comment is 250 characters ! ",category="warning")
                get_comments = comments.show_events_comments(id)
                return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)
            
            
            comments.add_comment(content,event_participant, event_id)
            get_comments = comments.show_events_comments(id)
            return render_template("event.html",event=event,author=author,participants=get_participants,comment=get_comments)

@app.route("/users/<int:id>",methods=["GET","POST"])
def search_users(id = None):
    if check_authorization(auth_level="login") == False:
        return redirect("/login")

    if request.method == "GET":
        return render_template("search_users.html",event_id=id)
    
    if request.method == "POST":
        users.authorization_csrf()
        searched_user = users.search_users(request.form["query"])

        if searched_user:
            uid = users.get_user_id_by_username(searched_user[0][0])[0][0]
            invite_user = users.invite_user_to_event(uid,id)
            
            if invite_user:
                flash(f"You have successfully invited user {searched_user[0][0]}",category="info")
            else:
                flash(f"User {searched_user[0][0]} has already been invited !",category="warning")
        else: 
            flash("No such user found! ",category="warning") 
            return render_template("search_users.html",event_id=id)
        
        return render_template("search_users.html",event_id=id)


@app.route("/attending_to", methods=["GET","POST"])
@app.route('/attending_to/<action>/<event_id>', methods=['GET', 'POST'])
def attending_to(action=None, event_id=None):
    if check_authorization(auth_level="login") == False:
        return redirect("/login")

    if request.method == "GET":
        attending_events = participants.get_events_from_participant(users.user_id())
        return render_template("attending.html",events=attending_events)

    if request.method == "POST":
        users.authorization_csrf()

        if action == "cancel_attendance":
            user_id = users.user_id()
            print(event_id,user_id)
            participants.cancel_attendance(user_id,event_id)
            event_name = events.get_event_name(event_id)
            flash(f"You have successfully cancelled your attendance to {event_name}! ",category="info")
            return redirect("/attending_to")
            
def check_authorization(auth_level, action=None,event_id=None):
    if auth_level=="login":
        if users.user_id() == 0:
            flash("Please login for such actions! ",category="warning")
            return False
    else: 
        if action != None and event_id != None:
            if events.get_event_author(event_id)[0][0] != users.get_username(users.user_id())[0][0]:
                flash("You are not authorized for such actions!",category="warning")
                return False
    return True
