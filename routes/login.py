from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.models import Record

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "admin123":
            session['authenticated'] = True
            return redirect(url_for('monitor_bp.monitor'))

        else:
            flash("Incorrect password", "danger")
    return render_template('login.html')
