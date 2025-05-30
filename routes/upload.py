import os
import numpy as np
from flask import Blueprint, request, render_template, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from db.models import db, Record
from utils.preprocessing import preprocess_image, is_low_entropy, is_uncertain
from config import model_session, class_labels, rejected_attempts
from skimage.measure import shannon_entropy
from db.models import Record

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    global rejected_attempts
    if not session.get('authenticated'):
        return redirect(url_for('login_bp.login'))

    doctor_name = request.args.get('doctor_name')
    patient_name = request.args.get('patient_name')
    patient_id = request.args.get('patient_id')

    prediction, confidence, image_preview, message = None, None, None, None
    valid_prediction = False

    if request.method == 'POST':
        file = request.files['image']
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            input_image, raw_image = preprocess_image(filepath)
            image_entropy = shannon_entropy(raw_image)

            if is_low_entropy(raw_image):
                message = f"Rejected: Low image entropy ({image_entropy:.2f})."
                rejected_attempts += 1
                os.remove(filepath)
            else:
                input_name = model_session.get_inputs()[0].name
                output = model_session.run(None, {input_name: input_image})
                probabilities = output[0][0]
                predicted_index = int(np.argmax(probabilities))
                confidence = float(np.max(probabilities)) * 100
                predicted_class = class_labels[str(predicted_index)]

                if confidence < 100 or is_uncertain(probabilities):
                    message = f"Rejected: Low confidence ({confidence:.2f}%) or uncertain prediction."
                    rejected_attempts += 1
                    os.remove(filepath)
                else:
                    prediction = predicted_class
                    image_preview = filename
                    valid_prediction = True
                    message = f"Predicted: {prediction} (Confidence: {confidence:.2f}%)"

                    new_record = Record(
                        doctor_name=doctor_name,
                        patient_name=patient_name,
                        patient_id=patient_id,
                        image_filename=filename,
                        prediction=prediction,
                        confidence=confidence
                    )
                    db.session.add(new_record)
                    db.session.commit()
        else:
            message = 'Invalid file type. Please upload PNG or JPG.'

    return render_template(
        'upload.html',
        doctor_name=doctor_name,
        patient_name=patient_name,
        patient_id=patient_id,
        prediction=prediction,
        confidence=confidence,
        message=message,
        image_preview=image_preview,
        valid_prediction=valid_prediction
    )
