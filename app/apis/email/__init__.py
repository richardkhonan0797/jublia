from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

email_bp = Blueprint("email", __name__, template_folder="templates")

app = Api(email_bp)
initialize_routes(app)