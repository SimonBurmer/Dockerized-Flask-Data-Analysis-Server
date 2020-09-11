
from flask import render_template, redirect, url_for, flash, session, request, Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models import User
from functools import wraps


flask_api = Blueprint('flask_api', __name__)

#this is a secure user validation 
def login_required_api(function):
    @wraps(function)#required when stacking wrapper
    def wrapper(*args, **kwargs):
        if  not "username" in session:
            # retruns none if user isn't a key in the dictionary (none is null in java)
            return "To get access to the API you have to loggin to xxx/login with username and password", 404
        else:
            return function(*args, **kwargs)
    return wrapper


@flask_api.route('/login',methods=["POST"])
def api_login():
    # /? username=<username> & password=<password> The URL parameters (data after ?) are available in request.args, which is an ImmutableMultiDict that has a get method
    username = request.args.get('username')
    userpassword = request.args.get('userpassword')
    found_user = User.query.filter_by(username=username).first()
    if found_user and  check_password_hash(found_user.userpassword,userpassword):
            session.permanent = True
            session["username"] = username
            return "you are logged in" , 200
    else:
            return "your login data is incorrect", 404


@flask_api.route('/user/<int:user_id>/',methods=["GET"])
@login_required_api
def get_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            #show error if no User id found
            return f"Could not find user with id = {user_id}", 404
        return jsonify({'id': user.id, 'name': user.username, 'password': user.userpassword})
    

@flask_api.route('/user',methods=["POST"])
@login_required_api
def post_user():
    # /? username=<username> & password=<password> The URL parameters (data after ?) are available in request.args, which is an ImmutableMultiDict that has a get method
    username = request.args.get('username')
    userpassword = request.args.get('userpassword')
    
    if not username or not userpassword: #if the key didn't exists --> username = None
        return jsonify('your request is not corret' ,{'username': 'name of the user' , 'userpassword':'Passwort of the User'}), 400


    user = User.query.filter_by(username=username).first()
    if user:
        return f"Username {username} already taken", 404
    else:
        print(userpassword)
        new_user = User(username= username, userpassword=generate_password_hash(userpassword))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'name': new_user.username, 'password': new_user.userpassword}), 201


