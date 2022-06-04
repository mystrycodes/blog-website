from http import client
from flask import Flask,render_template, request
import datetime
from pymongo import MongoClient

def create_app():

    app= Flask(__name__)
    client= MongoClient('mongodb+srv://afraz:afraz@microblog-application.gbjkl.mongodb.net/test')
    app.db=client.microblog

    @app.route('/', methods=['GET','POST'])
    def home():
        if request.method == 'POST':
            entry_content=request.form.get("content")
            formatted_date=datetime.datetime.today().strftime("%y-%m-%d")
            app.db.entries.insert_one({"content":entry_content,"date":formatted_date})
        entries_with_date=[
                (
                    entry['content'],
                    entry['date'],
                    datetime.datetime.strptime(entry['date'],"%y-%m-%d").strftime("%b %d")
                )
                for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries= entries_with_date)
    
    return app