from os import environ

import yagmail
from celery import Celery

MAIL_ID = environ.get("MAIL_ID")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")

yag = yagmail.SMTP(user=MAIL_ID, password=MAIL_PASSWORD)

redis_broker = f"redis://{environ.get('REDIS_HOST')}:6379"
celery_app = Celery("send email", broker=redis_broker, backend=redis_broker)


@celery_app.task
def send_without_attachment(
    recipient_email, subject="Prueba", message="Mensaje de Prueba."
):
    yag.send(to=recipient_email, subject=subject, contents=message)
