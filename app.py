import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.utils import secure_filename
from cs50 import SQL

from genome_analysis import analyze, compare

UPLOAD_FOLDER = "./vcfs"
ALLOWED_EXTENSIONS = set(["vcf"])

# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
	""""""
	if request.method == "GET":
		recipients = db.execute("SELECT * FROM recipients")
		return render_template("index.html", recipients=recipients)


@app.route("/match", methods=["GET", "POST"])
def match():
	""""""
	if request.method == "GET":
		recipients = db.execute("SELECT * FROM recipients")
		return render_template("search.html", recipients=recipients)
	elif request.method == "POST":
		recipient_id = request.form.get("id")
		print(recipient_id)
		recipient_info = db.execute("SELECT * FROM recipients WHERE id = :id", id=recipient_id)
		donors = db.execute("SELECT * FROM donors")
		return render_template("results.html", donors=donors)


@app.route("/upload", methods=["GET", "POST"])
def upload():
	if request.method == "GET":
		return render_template("upload.html")

	elif request.method == "POST":

		id = request.form.get("id")
		patient_type = request.form.get("patient_type")
		location = int(request.form.get("location"))
		age = request.form.get("age")

		if 'file' not in request.files:
				flash('No file part')
				return redirect(request.url)


		file = request.files["file"]

		print(id)
		print(patient_type)
		print(location)
		print(age)
		print(file)

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)


		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filepath = "./vcfs/" + filename
			# genotype = analyze(file_path)

			# if patient_type == "recipient":
			# 	# db.execute("INSERT INTO 'recipients' ('id','location') VALUES (:id, :location)", id=id, location=location)
			# 	# db.execute("INSERT INTO 'recipient_genotypes' ('id') VALUES (:id)", id=id)
			# 	# i = 1
			# 	# for gene in genotype:
			# 	# 	 db.execute("UPDATE 'recipient_genotypes' SET :column = :gene WHERE id = :id", column=i, gene=gene, id=id)
			# 	# 	 i = i + 1
			# else:
			# 	# db.execute("INSERT INTO 'donors' ('id','location') VALUES (:id, :location)", id=id, location=location)
			# 	# db.execute("INSERT INTO 'donor_genotypes' ('id') VALUES (:id)", id=id)
			# 	# i = 1
			# 	# for gene in genotype:
			# 	# 	 db.execute("UPDATE 'donor_genotypes' SET :column = :gene WHERE id = :id", column=i, gene=gene, id=id)
			# 	# 	 i = i + 1

			os.remove(filepath)
			flash('Upload Successful')
			return redirect(request.url)