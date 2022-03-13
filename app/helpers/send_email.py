import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from redis import Redis
from rq import Queue


def dequeue_email(email_subject, email_content, recipients, config):
    sender_address = config["host"]
    message = MIMEMultipart()
    message["From"] = config["host"]
    message["To"] = " ,".join(recipients)
    message["Subject"] = email_subject
    message.attach(MIMEText(email_content, 'html', 'utf-8'))
    session = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
    session.starttls()
    session.login(sender_address, config["pwd"])
    text = message.as_string()
    session.sendmail(sender_address, recipients, text)


def send_email(timestamp, email_subject, email_content, recipients):
    config = dict(
        host=os.environ.get("EMAIL_HOST"),
        pwd=os.environ.get("EMAIL_PASSWORD"),
        smtp_server=os.environ.get("SMTP_SERVER"),
        smtp_port=os.environ.get("SMTP_PORT")
    )

    q = Queue(
        connection=Redis(
            host=os.environ.get("REDIS_HOST"), 
            port=os.environ.get("REDIS_PORT"), 
            db=os.environ.get("REDIS_DB")
        )
    )

    res = q.enqueue_at(timestamp, dequeue_email, email_subject, email_content, recipients, config)
    return res
