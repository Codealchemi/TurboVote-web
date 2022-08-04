from flask import Flask, request, render_template
from flask_cors import CORS
from envelopes import Envelope
import toml, os, sys

from timeliner import TL

db = TL("data")

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("page.html", page="Home")

@app.route("/time/<where>", methods=["GET", "POST"])
def do_time(where):
    if request.method == "GET":
        if db.loc_exists(where):
            return str(db.get_time(where))
        else:
            return "No location " + where
    elif request.method == "POST":
        if db.loc_exists(where):
            db.post_time(where, request.json['time'])
            return "Done."
        else:
            return "No location " + where

@app.route("/location/<where>", methods=["GET", "POST"])
def location(where):
    if request.method == "GET":
        if db.loc_exists(where):
            return str(db.get_obj(where))
        else:
            return "No location " + where
    else: # post inferred
        if db.loc_exists(where):
            db.post_time(where, request.json['time'])
            return "Done."
        else:
            if 'desc' in request.json.keys(): # we can make a new location
                db.new_loc(where, request.json['desc'])
                returnt = "Made a new location '" + where + "' with desc of '" + request.json['desc'] + "'."
                if 'time' in request.json.keys(): # we can also post a time while we're at it
                    db.post_time(where, request.json['time'])
                    returnt += " Also posted an initial time of '" + request.json['time'] + "'."
                return returnt
            else: # no 'desc', can't make a new location
                return "Can't make a new location without 'desc' attribute."



@app.route("/list/locations")
def get_codes():
    return str(db.list_locations())