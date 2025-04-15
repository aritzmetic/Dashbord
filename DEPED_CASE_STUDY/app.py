import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from works import create_dash_apps  # This is your Dash app integration

app = Flask(__name__)

# Define upload paths and allowed file types
UPLOAD_FOLDER = 'static/uploads'
ACTIVE_DATASET = os.path.join(UPLOAD_FOLDER, 'active_dataset.csv')
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create the Dash apps (attach to this Flask app)
create_dash_apps(app)

# Helper function to validate CSV file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route — loads the active dataset and renders it
@app.route('/')
def home():
    if os.path.exists(ACTIVE_DATASET):
        try:
            if os.path.getsize(ACTIVE_DATASET) == 0:
                raise ValueError("CSV file is empty.")
            data = pd.read_csv(ACTIVE_DATASET)
            if data.empty:
                raise ValueError("CSV has no data.")
            print("Dataset loaded successfully.")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            data = pd.DataFrame()
    else:
        print("No dataset found.")
        data = pd.DataFrame()

    return render_template('index.html', data=data.to_dict(orient='records'))

# Upload route — receives the file and updates the active dataset
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('admin_panel'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('admin_panel'))

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'active_dataset.csv')
        file.save(filepath)
        os.replace(filepath, ACTIVE_DATASET)
        return redirect(url_for('home'))

    return 'File type not allowed', 400

# Admin panel page (CSV upload UI)
@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')

# Geographic view page
@app.route('/geographic_view')
def geographic_view():
    return render_template('geographic_view.html')

# Historical view page
@app.route('/historical_view')
def historical_view():
    return render_template('historical_view.html')

# Report generation page
@app.route('/generate_report')
def generate_report():
    return render_template('generate_report.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
