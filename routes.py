from app import app
from flask import render_template,request,redirect,url_for,session,flash

@app.route("/")
def index():
    return render_template('home.html')