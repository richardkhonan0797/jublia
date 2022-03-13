import traceback

from app import db
from dateutil import tz
from flask import (
    current_app,
    jsonify, 
    make_response, 
    request,
) 
from flask_restful import Resource
from flask_sieve import Validator

# Helpers import
from app.helpers.send_email import send_email

# Models import
from app.models.email_content_model import EmailContent
from app.models.email_recipient_model import EmailRecipient
from app.models.email_recipient_content_model import EmailRecipientContent


class SaveEmail(Resource):

    def post(self):
        try:
            rules = {
                "event_id": ["required", "integer"],
                "email_subject": ["required", "string"],
                "email_content": ["required", "string"],
                "timestamp": ["required", "date"]
            }

            validator = Validator(rules=rules, request=request)
            if validator.fails():
                response = {
                    "status": "error",
                    "status_code": 422,
                    "message": "validation_form_error",
                    "data": validator.messages(),
                }
                return make_response(jsonify(response), 422)
            else:
                body = request.get_json()

                new_email_content = EmailContent(
                    event_id=body.get("event_id"),
                    email_subject=body.get("email_subject"),
                    email_content=body.get("email_content"),
                    timestamp=body.get("timestamp")
                )

                db.session.add(new_email_content)
                db.session.commit()

                email_recipients = EmailRecipient.query.filter_by(event_id=body.get("event_id")).all()

                from_zone = tz.gettz("Asia/Singapore")
                to_zone = tz.tzlocal()
                timestamp = new_email_content.timestamp.replace(tzinfo=from_zone)
                new_timestamp = timestamp.astimezone(to_zone)

                if email_recipients:
                    recipients = [recipient.email_recipient for recipient in email_recipients]
                    job = send_email(
                        new_timestamp, 
                        body.get("email_subject"),
                        body.get("email_content"),
                        recipients
                    )

                    new_email_recipient_content = []
                    for recipient in email_recipients:
                        new_email_recipient_content.append(
                            EmailRecipientContent(
                                email_recipient_id = recipient.id,
                                email_content_id = new_email_content.id,
                                job_id = "rq:job:"+job.id
                            )
                        )
                    
                    db.session.add_all(new_email_recipient_content)
                    db.session.commit()

                db.session.close()
                
                response = {
                    "status": "success",
                    "status_code": 200,
                    "message": "success",
                    "data": body
                }
                return make_response(jsonify(response), 200)
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            response = {
                "status": "error",
                "status_code": 500,
                "message": "Internal Error",
                "data": {},
            }
            return make_response(jsonify(response), 500)
