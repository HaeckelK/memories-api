from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Memory(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=True, nullable=False)
    date_added = db.Column(db.Integer, unique=False, nullable=False)
