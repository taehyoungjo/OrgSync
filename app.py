from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from cs50 import SQL

from genome_analysis import analyze, compare

UPLOAD_FOLDER = "./vcfs"
ALLOWED_EXTENSIONS = set(["vcf"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQL("sqlite:///database.db")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    """"""
    if request.method == "GET":
        id = db.execute("SELECT id FROM donors")
        return render_template("index.html", id=id)

@app.route("/search", methods=["GET"])
def search():
    """"""
    if request.method == "GET":
        id = request.args.get("id")
        return render_template("search.html", id=id)

    elif request.method == "POST":
        return True

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

#        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#               filepath = "./vcfs/" + filename
#            genotype = analyze(file_path)
#
#            for gene in genotype:
#                db.execute("INSERT INTO ''")
#
#            os.remove(file_path)
#            return render_template("index.html")
