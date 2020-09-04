from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models import User
from functools import wraps


auth = Blueprint('auth', __name__)

#this is a secure user validation 
def login_required(function):
    @wraps(function)#required when stacking wrapper
    def wrapper(*args, **kwargs):
        if  not "username" in session:
            # retruns none if user isn't a key in the dictionary (none is null in java)
            flash("please login first", "info")
            return render_template("index.html")
        else:
            return function(*args, **kwargs)
    return wrapper


@auth.route("/login", methods=["POST"])
def login():
    username = request.form["nmHe"] #He because of header
    userpassword = request.form["pwHe"]
    #Checks if a user with the given username exists
    found_user = User.query.filter_by(username=username).first()
    if found_user and  check_password_hash(found_user.userpassword, userpassword):
        # Save Username in session
        # default is False, set it to True if you want the the session is saved as long as the permanent_session_lifetime is defined
        # If it is False, the session is saved as longe as you have opend your browser.
        session.permanent = True
        # to save someting in a Session / Session is a dic and i defined the dictionary key to be "user"
        session["username"] = username
        flash("You have been logged in!", "info")
        return redirect(url_for("main.profileGET"))
    else:
        flash("no User found", "info")
        return render_template("index.html")

@auth.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("main.home"))

@auth.route("/register",  methods=["GET"])
def registerGET():
    return render_template("register.html")

@auth.route("/register",  methods=["POST"])
def registerPOST():
    username = request.form["nmRe"]
    userpassword = request.form["pwRe"]
    if  User.query.filter_by(username=username).first():
        flash(f"Username {username} is already used!", "info")
        return redirect(url_for("auth.registerGET"))
    newUser = User(username=username, userpassword=generate_password_hash(userpassword))

    #Save new user in db
    db.session.add(newUser)
    db.session.commit()
    flash("You are registered!", "info")
    return render_template("index.html")