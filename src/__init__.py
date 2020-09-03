from .auth import auth
from flask import Flask
from datetime import timedelta
from .extensions import db
from .views import main
from .restFul_api import UserApi, UserListApi, UserLogin
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    db.init_app(app)

    #Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b2ce470d26edb7:3a20aa4d@eu-cdbr-west-03.cleardb.net/heroku_9e47351aae0ada8'

    app.secret_key ="b11c6$$$$$bb/6910c6e&6333a§49$25a()/b997)416cd76/0!8cd2c/6f28!cc!sfdyb?cd/d?20e0418db" #make sessions secure
    app.permanent_session_lifetime = timedelta(minutes = 5) #defines how long things are saved in the session

    #Register Blueprint
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    #Register REST-API
    api = Api(app)
    api.add_resource(UserApi, '/api/User/<int:userId>')
    api.add_resource(UserListApi, '/api/User')
    api.add_resource(UserLogin, '/api/Login')

    return app
