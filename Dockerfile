FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
COPY . .

# Install the dependencies
RUN pip install -r requirements.txt

#Needs Cloud to know which port to expose
EXPOSE 8080

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]