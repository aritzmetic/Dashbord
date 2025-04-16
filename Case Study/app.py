from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
import os
from works import create_dash_app
from report import create_dash_app_report
from data_config import get_dataset_path, fetch_summary_data_from_csv, fetch_enrollment_records_from_csv

app = Flask(__name__)
app.secret_key = 'secret123'

# Upload folder config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("account.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/enrollment")
def enrollment():
    return render_template("enrollment.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/year")
def year():
    return render_template("year.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, 'Cleaned_School_DataSet.csv'))
            flash('CSV file uploaded successfully and is now active!')
            return render_template("upload.html")

        flash("Invalid file type. Please upload a .csv file.")
        return redirect(request.url)

    return render_template("upload.html")

@app.route('/api/enrollment_data')
def get_enrollment_data():
    file_path = get_dataset_path()
    data = fetch_summary_data_from_csv(file_path)
    return jsonify(data)

# Mount Dash app
dash_app_works = create_dash_app(app)
dash_app_report = create_dash_app_report(app)

if __name__ == "__main__":
    app.run(debug=True)
