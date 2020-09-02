from src import create_app
from src.extensions import db

app = create_app()
createDb = False

# run the app. Docker needs this
if __name__ == "__main__":
    app.run(debug=False, port=8080, host='0.0.0.0') 

    if createDb:
        print("Creating database tables...")
        db.create_all()  #Creates all tables 
        print("Done!")
