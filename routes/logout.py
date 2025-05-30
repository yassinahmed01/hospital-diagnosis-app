from flask import Blueprint, session, redirect, url_for, flash
from db.models import Record

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout')
def logout():
    session.pop('authenticated', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('home_bp.home'))  # Adjust this if your home blueprint is named differently
