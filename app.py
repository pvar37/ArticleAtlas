import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import csv
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Load main page with the globe
@app.route("/")
def index():

    # Create a 2d array with each row being a country, and columns being things like name, longitude, latititude, etc. This is found in countries.csv
    structure = []
    file = open('countries.csv', 'r', newline='')
    data = csv.reader(file)
    for row in data:
        structure.append(row)
    file.close()

    # Render the globe page
    return render_template("globe.html", structure=structure)

# Render the about page
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
