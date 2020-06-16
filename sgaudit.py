#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    bg_color = "AliceBlue;"
    return render_template("index.html")