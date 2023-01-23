import os
from os import path
from cs50 import SQL
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

path = "/Users/stefanberger/Desktop/sportradar/database.db"
isExist = os.path.exists(path)

if isExist == False:
    db = sqlite3.connect("database.db", check_same_thread=False)
    db = SQL("sqlite:///database.db")
    db.execute(
        "CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, event TEXT, date DATETIME, game TEXT)"
    )
else:
    db = SQL("sqlite:///database.db")


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        date_input = request.form.get("date")
        event_input = request.form.get("event")
        game_input = request.form.get("game")

        db.execute(
            "INSERT into events (date, event, game) VALUES (?, ?, ?)",
            date_input,
            event_input,
            game_input,
        )

        category_db = db.execute("SELECT event FROM events GROUP BY event")

        events_db = db.execute("SELECT date, event, game FROM events")

        return render_template("index.html", events=events_db, categories=category_db)

    else:

        events_db = db.execute("SELECT date, event, game FROM events")

        category_db = db.execute("SELECT event FROM events GROUP BY event")

        return render_template("index.html", events=events_db, categories=category_db)
