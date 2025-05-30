import os
from flask import Blueprint, session, redirect, url_for, flash, current_app
from db.models import db, Record  

# Define Blueprint
delete_bp = Blueprint('delete_bp', __name__)

@delete_bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    # Authentication check
    if not session.get('authenticated'):
        return redirect(url_for('login_bp.login'))

    # Retrieve the record
    record = Record.query.get_or_404(record_id)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], record.image_filename)

    # Delete the image if it exists
    if os.path.exists(image_path):
        os.remove(image_path)

    # Remove record from database
    db.session.delete(record)
    db.session.commit()

    # Notify user
    flash("Record deleted successfully.", "success")
    return redirect(url_for('monitor_bp.monitor'))
