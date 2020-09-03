from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from .models import User, Note
from .extensions import db
from .auth import login_required

main = Blueprint("main", __name__, static_folder = "static", template_folder = "templates")


#methods=["POST", "GET"] To specify that a page works with both POST and GET requests
@main.route("/",  methods=["GET"])
def home():
    # you can define a html-file as .jinja to get jinja syntax-highliting
    return render_template("index.html")


@main.route("/user", methods=["POST", "GET"])
@login_required
def showUser():
    users = User.query.all()
    #session["users"] = users
    return render_template("user.html",users=users)


@main.route("/profile", methods=["GET"])
@login_required
def profileGET():
    note = ""
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    if user.notes:
        userNotes = user.notes
        return render_template("profile.html", userNotes=userNotes)
    return render_template("profile.html")


@main.route("/profile", methods=["POST"])
@login_required
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

