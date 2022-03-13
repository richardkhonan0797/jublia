from toml import load
from app import ma
from marshmallow import fields, Schema

class EmailContentSchema(Schema):
    id = fields.Int()
    event_id = fields.Int(required=True)
    email_subject = fields.Str(required=True)
    email_content = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)
    created_at = fields.DateTime(load_only=True)
    updated_at = fields.DateTime(load_only=True)