import os
from app import app
from flask import render_template, request, redirect

#need to install dnspython and flask_pymongo
username = "period 8"

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"},
        {"event": "Summer Vacation", "date":"2020-06-03"}
    ]


from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'test'


# URI of database
#taken from mongodb website
app.config['MONGO_URI'] = 'mongodb+srv://admin:teesi5o1gOex2h5G@cluster0-n5tzk.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    #connects to the database
    events = mongo.db.events
    #searches for all entries in the database
    events = list(events.find({}))
    #loads index.html
    return render_template('index.html', events = events)

@app.route('/input')
def input():
    #loads input.html
    return render_template('input.html')

@app.route('/results', methods = ['Get','Post'])
def results():
    #places the input recieved in a dictionary
    userdata = dict(request.form)
    #names the input recieved from the form
    event_name = userdata['name']
    event_date = userdata['date']
    username = userdata['username']
    #connects to the database
    events = mongo.db.events
    events.insert({'name':event_name, 'date':event_date})
    #searches for all entries in the database
    events = list(events.find({}))
    #loads index.html
    return render_template('index.html', events = events, username = username)

@app.route('/deleteAll', methods = ['Get','Post'])
def deleteAll():

    userdata = dict(request.form)
    #names password collected from form as password
    password = userdata['password']
    if password == "clearit!":
        #connects to the database
        collection = mongo.db.events
        #deletes all entries in the database
        collection.delete_many({})
        #loads deleteAll.html
        return render_template("deleteAll.html", password = password)
    else:
        return "incorrect password"
