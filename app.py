from src import create_app

app = create_app()


# run the app. Docker needs this
if __name__ == "__main__":
    app.run(debug=False, port=8080, host='0.0.0.0') 