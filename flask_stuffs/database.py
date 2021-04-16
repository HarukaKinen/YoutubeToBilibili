from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class channel(db.Model):
    channel_id = db.Column(db.String(255), primary_key=True)
    subscribe_mode = db.Column(db.String(255))

class tasks(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    status = db.Column(db.Integer, default=1)