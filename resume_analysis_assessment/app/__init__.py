import os
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Setup the folder to save uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Avoid circular imports: Import routes here
from app import routes
