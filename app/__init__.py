from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def init_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .models import (
        email_content_model,
        email_recipient_model,
        email_recipient_content_model
    )

    from app.apis.email import email_bp

    app.register_blueprint(email_bp)

    return app