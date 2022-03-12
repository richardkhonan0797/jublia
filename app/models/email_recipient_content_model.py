from app import db


class EmailRecipientContent(db.Model):
    __tablename__ = "email_recipient_content"
    id = db.Column(db.Integer, primary_key=True)
    email_recipient_id = db.Column(db.Integer, db.ForeignKey("email_recipient.id"))
    email_content_id = db.Column(db.Integer, db.ForeignKey("email_content.id"))
    job_id = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

    email_recipient = db.relationship("EmailRecipient", lazy="joined")
    email_content = db.relationship("EmailContent", lazy="joined")