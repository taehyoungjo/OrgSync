import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.utils import secure_filename
from tempfile import mkdtemp
from cs50 import SQL

from genome_analysis import analyze, compare

UPLOAD_FOLDER = "./vcfs"
ALLOWED_EXTENSIONS = set(["vcf"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQL("sqlite:///database.db")

@app.route("/", methods=["GET", "POST"])
def index():
    """"""
    if request.method == "GET":
        id = db.execute("SELECT id FROM donors")
        return render_template("index.html", id=id)

@app.route("/search", methods=["GET", "POST"])
def search():
    """"""
    if request.method == "GET":
        id = request.args.get("id")
        donor_info = db.execute("SELECT * FROM recipients")
        recipients_info = db.execute("SELECT * FROM donors WHERE id=:id", id=id)
        donor = db.execute("SELECT * FROM donor_genotypes WHERE id=:id", id=id)
        recipients = db.execute("SELECT * FROM recipient_genotypes")
        matches = compare(donor, recipients)
        return render_template("search.html", donor=donor, matches=matches)

    elif request.method == "POST":
    	return render_template("search.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
	if request.method == "GET":
		return render_template("upload.html")

	elif request.method == "POST":

		id = int(request.form.get("id"))

		location = int(request.form.get("location"))

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		file = request.files["file"]

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filepath = "./vcfs/" + filename

			# genotype = analyze(file_path)

			# db.execute("INSERT INTO 'recipients' ('id','location') VALUES (:id, :location)", id=id, location=location)
			# db.execute("INSERT INTO 'recipient_genotypes' ('id') VALUES (:id)", id=id)
			# i = 1

			# for gene in genotype:
			# 	 db.execute("UPDATE 'recipient_genotypes' SET :column = :gene WHERE id = :id", column=i, gene=gene, id=id)
			# 	 i = i + 1

			# os.remove(file_path)
			flash('Upload Successful')
			return redirect(request.url)