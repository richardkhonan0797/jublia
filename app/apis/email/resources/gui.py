import traceback

from app import db
from dateutil import tz
from flask import (
    current_app,
    jsonify, 
    make_response,
    render_template, 
    request,
) 
from flask_restful import Resource

# Models import
from app.models.email_content_model import EmailContent
from app.models.email_recipient_model import EmailRecipient
from app.models.email_recipient_content_model import EmailRecipientContent


class Gui(Resource):

    def get(self):
        return make_response(render_template("gui.html"), 200)