from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from .models import User, Note
from .extensions import db

main = Blueprint("main", __name__, static_folder = "static", template_folder = "templates")

@main.route("/",  methods=["GET"])
def home():
    # you can define a html-file as .jinja to get jinja syntax-highliting
    return render_template("index.html")


@main.route("/login", methods=["POST"])# methods=["POST", "GET"] To specify that a page works with both POST and GET requests
def login():
    username = request.form["nmHe"] #He because of header
    userpassword = request.form["pwHe"]

    # get User from db
    found_user = User.query.filter_by(username=username).first()
    if found_user:
        if found_user.userpassword == userpassword:
            # Save Username in session
            # default is False, set it to True if you want the the session is saved as long as the permanent_session_lifetime is defined
            # If it is False, the session is saved as longe as you have opend your browser.
            session.permanent = True
            # to save someting in a Session / Session is a dic and i defined the dictionary key to be "user"
            session["username"] = username
            flash("You have been logged in!", "info")
            return render_template("index.html")
    else:
        flash("no User found", "info")
        return render_template("index.html")

@main.route("/logout")
def logout():
    if "username" in session:
        # retruns none if user isn't a key in the dictionary (none is null in java)
        session.pop("username", None)
        flash("You have been logged out!", "info")
    # Importend! here index.X
    return redirect(url_for("main.home")) # the better solution would be return render_template("index.html")




@main.route("/register",  methods=["GET"])
def registerGET():
    return render_template("register.html")

@main.route("/register",  methods=["POST"])
def registerPOST():
    username = request.form["nmRe"]
    userpassword = request.form["pwRe"]
    newUser = User(username=username, userpassword=userpassword)

    #Save new user in db
    db.session.add(newUser)
    db.session.commit()
    flash("You are registered!", "info")
    return render_template("index.html")




@main.route("/user", methods=["POST", "GET"])
def user():
    users = User.query.all()
    #session["users"] = users
    return render_template("user.html",users=users)

@main.route("/profile", methods=["GET"])
def profileGET():
    note = ""
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    if user.notes:
        userNotes = user.notes
        return render_template("profile.html", userNotes=userNotes)
    return render_template("profile.html")

@main.route("/profile", methods=["POST"])
def profilePOST():
    note = request.form["note"]
    noteTitle = request.form["title"]
    username = session["username"]

    user = User.query.filter_by(username=username).first()

    newNote = Note(person_id = user.id, note=note, noteTitle=noteTitle)
    db.session.add(newNote)
    db.session.commit()

    flash("Your note is saved!", "info")
    return redirect(url_for("main.profileGET"))

