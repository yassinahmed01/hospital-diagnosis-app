from flask import Blueprint, render_template, request, redirect, url_for
from db.models import Record

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name')
        patient_name = request.form.get('patient_name')
        patient_id = request.form.get('patient_id')

        return redirect(url_for('upload_bp.upload', doctor_name=doctor_name, patient_name=patient_name, patient_id=patient_id))

    return render_template('index.html')
