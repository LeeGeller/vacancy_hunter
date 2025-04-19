from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255),)
    description = db.Column(db.Text,)
    schedule_type = db.Column(db.String(255))
    salary_from = db.Column(db.Integer,)
    salary_to = db.Column(db.Integer,)
    currency = db.Column(db.String(20))
    url = db.Column(db.String)