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
from app.helpers.redis import delete_multiple

# Models import
from app.models.email_content_model import EmailContent
from app.models.email_recipient_model import EmailRecipient
from app.models.email_recipient_content_model import EmailRecipientContent


class ManageEmail(Resource):

    def delete(self):
        try:
            rules = {
                "email_content_id": ["required", "string"]
            }

            validator = Validator(rules=rules, request=request.args)
            if validator.fails():
                response = {
                    "status": "error",
                    "status_code": 422,
                    "message": "validation_form_error",
                    "data": validator.messages(),
                }
                return make_response(jsonify(response), 422)
            else:
                email_content_id = int(request.args.get("email_content_id"))
                email_recipient_content = EmailRecipientContent.query.filter_by(email_content_id=email_content_id).all()

                job_ids = ["rq:job:"+erc.job_id for erc in email_recipient_content]
                if job_ids:
                    delete_multiple(job_ids)

                EmailRecipientContent.query.filter_by(email_content_id=email_content_id).delete()
                EmailContent.query.filter_by(id=email_content_id).delete()

                db.session.commit()
                db.session.close()

                response = {
                    "status": "success",
                    "status_code": 200,
                    "message": "success",
                    "data": {}
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
