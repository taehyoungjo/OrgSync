from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """"""
    if request.method == "GET":
        return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """"""
    if request.method == "GET":
        return render_template("upload.html")

@app.route("/search", methods=["GET"])
def search():
    """"""
    if request.method == "GET":
        id = request.args.get("id")
        return render_template("search.html", id=id)