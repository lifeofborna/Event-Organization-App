from flask import Flask
from flask import redirect, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import routes