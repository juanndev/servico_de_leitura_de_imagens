from app import db

class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measure_uuid = db.Column(db.String(36), unique=True, nullable=False)
    customer_code = db.Column(db.String(50), nullable=False)
    measure_datetime = db.Column(db.DateTime, nullable=False)
    measure_type = db.Column(db.String(10), nullable=False)
    measure_value = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    is_confirmed = db.Column(db.Boolean, default=False)
