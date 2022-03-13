import os

class Config(object):
    APP_DEBUG = os.environ.get("APP_DEBUG", False)
    APP_PORT = os.environ.get("APP_PORT")

    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    REDIS_DB = os.environ.get("REDIS_DB")
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=os.environ.get("POSTGRES_USER"),
        pw=os.environ.get("POSTGRES_PW"),
        url=os.environ.get("POSTGRES_URL"),
        db=os.environ.get("POSTGRES_DB"),
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    SMTP_PORT = os.environ.get("SMTP_PORT")