from flask import Flask, request, render_template, redirect
from flask_cors import CORS
from envelopes import Envelope
import toml, os, sys

from timeliner import TL

db = TL("localhost", 4040, "7dd30892-a7a9-4343-bab0-1cdf6575a201")

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
            obj = db.get_obj(where)
            embed = "<h2>Location description: " + str(obj['data']['data']['desc']) + "</h2>"
            embed += "<h3>Recorded times:</h3>"
            times = obj['data']['data']['times']
            if len(times) != 0:
                for time in reversed(times):
                    embed += "<p>- " + str(time) + "</p>"
            else:
                embed += "<p style='color:red;'>No recorded times.</p>"
            embed += render_template("submit_time.html")
            return render_template("page.html", page="Information for location " + str(where), raw=embed)
        else:
            return render_template("page.html", page="Error", raw="<p>No location " + where + "</p>")
    else: # post inferred
        if db.loc_exists(where):
            res = db.post_time(where, request.form['new_time'])
            if "new time" in res:
                return redirect("/location/" + where)
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

@app.route("/useragent")
def get_ua():
    return str(request.headers.get('User-Agent'))