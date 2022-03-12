from app import db


class EmailContent(db.Model):
    __tablename__ = "email_content"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    email_subject = db.Column(db.String)
    email_content = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())
