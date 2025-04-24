from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
from flask import jsonify
from werkzeug.utils import secure_filename
from charts import generate_bar_chart
import base64
import matplotlib.pyplot as plt
from charts import CHART_FUNCTIONS

import uuid
from datetime import timedelta





app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        session['email'] = email
        return redirect(url_for('home_page'))
    return "Please enter both email and password.", 400

@app.route('/home')
def home_page():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', preview_table=None)

def generate_preview(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)  # Adjust this for Excel or CSV format
    preview = data.head().to_html()  # Display the first few rows as an HTML table
    return preview

DATA = {}
CHARTS = {}

import uuid

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded."

        file = request.files['file']
        if file.filename == '':
            return "No selected file."

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load dataset
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(filepath)
        else:
            return "Unsupported file format."

        # Store in-memory and session
        session_id = session.get('id', 'default')
        DATA[session_id] = df
        session['data_uploaded'] = True  # Mark dataset uploaded

        # Preview for modal
        preview = df.head().to_html(classes="table table-bordered")
        return render_template('dashboard.html', preview=preview, show_modal=True)

    return render_template('dashboard.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Get session ID from request
    data = request.get_json()
    session_id = session.get('id', 'default')  # Use server-side session ID
    
    # Debug print (remove later)
    print("Current session ID:", session_id)
    print("Stored data keys:", DATA.keys())

    if session_id not in DATA:
        return jsonify({
            'success': False, 
            'error': 'Dataset not found. Please re-upload your data.'
        })

    try:
        df = DATA[session_id]
        chart_type = data.get('chart_type')
        
        # Debug print
        print("Generating:", chart_type, "with df shape:", df.shape)

        buf = CHART_FUNCTIONS[chart_type](
            df,
            colors=data.get('color', '#3366CC'),
            style=data.get('style', 'classic')
        )

        # Save chart
        chart_id = uuid.uuid4().hex
        chart_path = f"static/charts/{chart_id}.png"
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        
        with open(chart_path, 'wb') as f:
            f.write(buf.getvalue())  # Use getvalue() for BytesIO

        return jsonify({
            'success': True,
            'chart_html': f'<img src="/{chart_path}" class="chart-img">'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    
if __name__ == '__main__':
    app.run(debug=True)

    