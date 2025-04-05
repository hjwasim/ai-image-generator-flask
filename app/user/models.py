from .. import db

class UserPrompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    prompt = db.Column(db.String(255), nullable=False)