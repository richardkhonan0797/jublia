from app import db


class EmailRecipient(db.Model):
    __tablename__ = "email_recipient"
    id = db.Column(db.Integer, primary_key=True)
    email_recipient = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())
