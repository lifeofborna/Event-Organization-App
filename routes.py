from unicodedata import category
from app import app
from flask import render_template,request,redirect,url_for,session,flash
import users

@app.route("/")
def index():
    return render_template('home.html')

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
        ##Todo pop a error html page
        flash("Wrong credentials")
        return render_template("login.html",category='warning')



@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")