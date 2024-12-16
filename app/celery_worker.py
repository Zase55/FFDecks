from os import environ

import yagmail
from celery import Celery

MAIL_ID = environ.get("MAIL_ID")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")

yag = yagmail.SMTP(user=MAIL_ID, password=MAIL_PASSWORD)

redis_broker = f"redis://{environ.get('REDIS_HOST')}:6379"
celery_app = Celery("send email", broker=redis_broker, backend=redis_broker)


@celery_app.task(bind=True)
def send_without_attachment(self, recipient_email, subject, message):
    try:
        yag.send(to=recipient_email, subject=subject, contents=message)
        return f"Correo enviado a {recipient_email}"
    except Exception as e:
        self.retry(exc=e, countdown=60, max_retries=3)  # Reintentar si falla
