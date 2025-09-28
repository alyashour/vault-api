import os
import smtplib 
from dotenv import load_dotenv
from email.message import EmailMessage 

from logger import logger 

load_dotenv()

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
APP_PASSWORD = os.getenv('APP_PASSWORD')

if not EMAIL_FROM or not EMAIL_TO or not APP_PASSWORD:
    raise Exception(f'Failed to load .env variables please check .env is provided and try again.')

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_FROM, APP_PASSWORD)
            smtp.send_message(msg)
        logger.info(f'Email sent: {subject}')
    except Exception as e:
        logger.error(f'Failed to send email \'{subject}\': {e}')