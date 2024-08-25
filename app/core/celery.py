import smtplib
import os

from email.message import EmailMessage

from celery import Celery
from dotenv import load_dotenv



load_dotenv(dotenv_path='.env')

celery = Celery('registration', broker=os.getenv('REDIS_HOST'))

def get_greeting_email_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Регистрация на сервисе бронирования переговорок'
    email['From'] = os.getenv('SMTP_USER')
    email['To'] = os.getenv('SMTP_USER')

    email.set_content(
        f"""<div class="container">
            <h1>Привет, {username}!</h1>
            <p>Мы рады приветствовать тебя на нашем сервисе!</p>
        </div>""",
        subtype='html',
    )
    return email

@celery.task
def send_greeting_email(username: str):
    email = get_greeting_email_dashboard(username)
    with smtplib.SMTP_SSL(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT')) as server:
        server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        server.send_message(email)
