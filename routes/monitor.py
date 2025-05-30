from flask import Blueprint, render_template, session, redirect, url_for, current_app
import os
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from collections import Counter
from db.models import Record
from config import rejected_attempts
from db.models import Record

monitor_bp = Blueprint('monitor_bp', __name__)

@monitor_bp.route('/monitor')
def monitor():
    if not session.get('authenticated'):
        return redirect(url_for('login_bp.login'))

    records = Record.query.order_by(Record.timestamp.desc()).all()
    predictions = [r.prediction for r in records]
    counts = Counter(predictions)

    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 12})
    chart_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'chart.png')
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

    return render_template(
        'monitor.html',
        records=records,
        counts=counts,
        chart_url=chart_path,
        rejected_count=rejected_attempts
    )
