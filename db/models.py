from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Define Cairo timezone
egypt = timezone('Africa/Cairo')

# Record model for storing classification records
class Record(db.Model):
    __tablename__ = 'records'  

    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(egypt), nullable=False)

    def __repr__(self):
        return f"<Record {self.id} - {self.patient_name} - {self.prediction}>"
