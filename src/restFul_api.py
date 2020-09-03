from flask_restful import reqparse, abort, Resource, marshal_with, fields
from flask import session
from .models import User
from .extensions import db 
from functools import wraps
from werkzeug.security import check_password_hash


# Argument Parsing -- is a built-in support for request data validation
User_put_args = reqparse.RequestParser()
User_put_args.add_argument("username", type=str, help="Name of the User", required=True)
User_put_args.add_argument("userpassword", type=str, help="Password of the User", required=True)

User_update_args = reqparse.RequestParser()
User_update_args.add_argument("username", type=str, help="Name of the User")
User_update_args.add_argument("userpassword", type=str, help="Passwort of the User")

User_login_args = reqparse.RequestParser()
User_login_args.add_argument("username", type=str, help="Name of the User", required=True)
User_login_args.add_argument("userpassword", type=str, help="Password of the User", required=True)


# The fields module is used to describe the structure of your response.
resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'userpassword': fields.String,
}


#this is a secure user validation 
def login_required_api(function):
    @wraps(function)#required when stacking wrapper
    def wrapper(*args, **kwargs):
        if  not "username" in session:
            # retruns none if user isn't a key in the dictionary (none is null in java)
            abort(404, message="To get access to the API you have to loggin ")
        else:
            return function(*args, **kwargs)
    return wrapper


class UserLogin(Resource):
    def post(self):
        args = User_login_args.parse_args()
        found_user = User.query.filter_by(username=args["username"]).first()
        if found_user and  check_password_hash(found_user.userpassword,args["userpassword"]):
            session.permanent = True
            session["username"] = args["username"]
            return "you are logged in" , 200
        else:
            abort(404, message="your data is incorrect")


class UserApi(Resource):
    # The above example takes a python object and prepares it to be serialized.
    # The marshal_with() decorator will apply the transformation described by resource_fields
    @marshal_with(resource_fields)
    #you have to register the userID variable in __init__ --> api.add_resource(UserApi, '/api/User<int:userId>')
    @login_required_api
    def get(self, userId):
        user = User.query.filter_by(id=userId).first()
        if not user:
            #show error if no User id found
            abort(404, message="Could not find user with id = {}".format(userId))
        return user
    
    @marshal_with(resource_fields)
    @login_required_api
    def delete(self, userId):
        user = User.query.filter_by(id=userId).first()
        if not user:
            abort(404, message="Could not find user with id = {}".format(userId))
        db.session.delete(user)
        db.session.commit()
        #204 --> No Content --> Die Anfrage wurde erfolgreich durchgeführt, die Antwort enthält jedoch bewusst keine Daten.
        return '', 204
    
    @marshal_with(resource_fields)
    @login_required_api
    def put(self, userId):
        #get arguments from RequestParser --> args is a dictionary
        args = User_put_args.parse_args()
        user = User.query.filter_by(id=userId).first()
        if user:
            db.session.delete(user)
        newUser = User(id=userId, username=args["username"], userpassword=args["userpassword"])
        db.session.add(newUser)
        db.session.commit()
        #201 --> Created
        return newUser, 201


class UserListApi(Resource):
    @marshal_with(resource_fields)
    @login_required_api
    def get(self):
        users = User.query.all()
        return users
    
    @marshal_with(resource_fields)
    @login_required_api
    def post(self):
        args = User_put_args.parse_args()
        user = User.query.filter_by(username=args["username"]).first()
        if user:
            abort(404, message="Username {} already taken".format(args["username"]))
        newUser = User(username=args["username"], userpassword=args["userpassword"])
        db.session.add(newUser)
        db.session.commit()
        return newUser, 201
