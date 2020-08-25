from .extensions import db

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship('Note', backref='user', lazy=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    userpassword= db.Column(db.String(120), unique=False, nullable=False)

    # __init__ is not mandatory!
    # Note how we never defined a __init__ method on the User class? 
    # That’s because SQLAlchemy adds an implicit constructor to all 
    # model classes which accepts keyword arguments for all its columns and relationships.

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    note = db.Column(db.String(200), nullable=False)
    noteTitle = db.Column(db.String(200), nullable=True)



if __name__ == "__main__":
    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()  #Creates all tables 
    print("Done!")
