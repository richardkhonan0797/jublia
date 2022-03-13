import traceback

from datetime import datetime
from dateutil import tz
from app import db
from email import message
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


class SaveRecipient(Resource):

    def post(self):
        try:
            rules = {
                "event_id": ["required", "integer"],
                "email_recipient": ["required", "email"],
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

                email_recipient = (
                    EmailRecipient.query.
                    filter_by(
                        event_id=body.get("event_id"), 
                        email_recipient=body.get("email_recipient")
                    ).
                    count()
                )

                from_zone = tz.tzlocal()
                to_zone = tz.gettz("Asia/Singapore")
                timestamp = datetime.now().replace(tzinfo=from_zone)
                sg_timestamp = timestamp.astimezone(to_zone)

                upcoming_email = (
                    EmailContent.query.
                    filter(
                        EmailContent.event_id==body.get("event_id"),
                        EmailContent.timestamp >= sg_timestamp
                    ).
                    all()
                )

                if not email_recipient:
                    new_email_recipient = EmailRecipient(
                        event_id=body.get("event_id"),
                        email_recipient=body.get("email_recipient")
                    )

                    db.session.add(new_email_recipient)
                    db.session.commit()

                    if upcoming_email:
                        from_zone = tz.gettz("Asia/Singapore")
                        to_zone = tz.tzlocal()

                        new_email_recipient_content = []
                        for email in upcoming_email:
                            timestamp = email.timestamp.replace(tzinfo=from_zone)
                            new_timestamp = timestamp.astimezone(to_zone)
                            job = send_email(
                                new_timestamp, 
                                email.email_subject,
                                email.email_content,
                                [new_email_recipient.email_recipient]
                            )
                            new_email_recipient_content.append(
                                EmailRecipientContent(
                                    email_recipient_id=new_email_recipient.id,
                                    email_content_id=email.id,
                                    job_id="rq:job:"+job.id
                                )
                            )
                        db.session.add_all(new_email_recipient_content)
                        db.session.commit()

                    db.session.close()
                
                response = {
                    "status": "success",
                    "status_code": 200,
                    "message": "SUCCESS",
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
