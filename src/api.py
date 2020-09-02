from flask_restful import reqparse, abort, Resource, marshal_with, fields
from .models import User, Note
from .extensions import db 


# Argument Parsing -- is a built-in support for request data validation
User_put_args = reqparse.RequestParser()
User_put_args.add_argument("username", type=str, help="Name of the User", required=True)
User_put_args.add_argument("userpassword", type=str, help="Password of the User", required=True)

User_update_args = reqparse.RequestParser()
User_update_args.add_argument("username", type=str, help="Name of the User")
User_update_args.add_argument(
    "userpassword", type=str, help="Passwort of the User")


# The fields module is used to describe the structure of your response.
resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'userpassword': fields.String,
}

class UserApi(Resource):

    # The above example takes a python object and prepares it to be serialized.
    # The marshal_with() decorator will apply the transformation described by resource_fields
    @marshal_with(resource_fields)
    #you have to register the userID variable in __init__ --> api.add_resource(UserApi, '/api/User<int:userId>')
    def get(self, userId):
        user = User.query.filter_by(id=userId).first()
        if not user:
            #show error if no User id found
            abort(404, message="Could not find user with id = {}".format(userId))
        return user
    
    @marshal_with(resource_fields)
    def delete(self, userId):
        user = User.query.filter_by(id=userId).first()
        if not user:
            abort(404, message="Could not find user with id = {}".format(userId))
        db.session.delete(user)
        db.session.commit()
        #204 --> No Content --> Die Anfrage wurde erfolgreich durchgeführt, die Antwort enthält jedoch bewusst keine Daten.
        return '', 204
    
    @marshal_with(resource_fields)
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
    def get(self):
        users = User.query.all()
        return users
    
    @marshal_with(resource_fields)
    def post(self):
        args = User_put_args.parse_args()
        user = User.query.filter_by(username=args["username"]).first()
        if user:
            abort(404, message="Username {} already taken".format(args["username"]))
        newUser = User(username=args["username"], userpassword=args["userpassword"])
        db.session.add(newUser)
        db.session.commit()
        return newUser, 201
