from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.utils import secure_filename

from genome_analysis import analyze


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
        
    elif request.method == "POST":
    	vcfFile = request.files["file"]
    	filename = secure_filename(vcfFile.filename)
    	vcfFile.save(os.path.join('./vcfs', filename))
    	file_path = "./vcfs/" + filename
    	genotype = analyze(file_path)
    	os.remove(file_path)
    	


@app.route("/upload", methods=["GET", "POST"])
def upload():
	if request.method == "GET":
		return render_template("upload.html")
	elif request.method == "POST"
