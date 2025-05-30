import os
import pandas as pd
from flask import Blueprint, session, redirect, url_for, send_file, current_app
from db.models import Record  

export_bp = Blueprint('export_bp', __name__)

@export_bp.route('/export')
def export_records():
    if not session.get('authenticated'):
        return redirect(url_for('login_bp.login'))

    # Retrieve and format the records
    records = Record.query.order_by(Record.timestamp.desc()).all()
    data = [{
        'ID': r.id,
        'Doctor': r.doctor_name,
        'Patient': r.patient_name,
        'Patient ID': r.patient_id,
        'Prediction': r.prediction,
        'Confidence': f"{r.confidence:.2f}%",
        'Timestamp': r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for r in records]

    # Use app config for upload folder
    export_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'exported_records.csv')
    pd.DataFrame(data).to_csv(export_path, index=False)

    return send_file(export_path, as_attachment=True)
