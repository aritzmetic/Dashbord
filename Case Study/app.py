from flask import Flask, render_template, request, redirect, flash, jsonify
import os
from works import create_dash_app
from data_config import get_dataset_path, fetch_enrollment_data_from_csv

app = Flask(__name__)
app.secret_key = 'secret123'

# Upload folder config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/enrollment")
def enrollment():
    return render_template("enrollment.html")

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
    data = fetch_enrollment_data_from_csv(file_path)
    return jsonify(data)

# Mount Dash app
dash_app = create_dash_app(app)

if __name__ == "__main__":
    app.run(debug=True)