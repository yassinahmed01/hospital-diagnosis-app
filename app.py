import os
import json
from datetime import datetime
from pytz import timezone
import matplotlib
matplotlib.use('Agg')  
from collections import Counter
from flask import Flask, render_template, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
import onnxruntime as ort

from db.models import db  
from utils.preprocessing import allowed_file, preprocess_image, is_uncertain, is_low_entropy
from db.models import db, Record  # 

# Flask App Config 
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Folder Setup 
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('instance', exist_ok=True)

# Initialize DB 
db.init_app(app)

# Globals 
model_session = ort.InferenceSession("densenet121_model.onnx")
with open("class_names.json", "r") as f:
    class_labels = json.load(f)

rejected_attempts = 0
egypt = timezone('Africa/Cairo')

# Register Blueprints
from routes.home import home_bp
from routes.upload import upload_bp
from routes.login import login_bp
from routes.monitor import monitor_bp
from routes.export import export_bp
from routes.delete_record import delete_bp
from routes.logout import logout_bp

app.register_blueprint(home_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(login_bp)
app.register_blueprint(monitor_bp)
app.register_blueprint(export_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(logout_bp)

# Run App 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

