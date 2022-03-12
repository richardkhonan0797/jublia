from .resources.save_email import SaveEmail
from .resources.save_recipient import SaveRecipient

def initialize_routes(api):
    api.add_resource(SaveEmail, "/save_emails")
    api.add_resource(SaveRecipient, "/save_recipient")