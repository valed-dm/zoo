import time

from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def get_metrics(url, method):
    time.sleep(60)
    print("request method:", method, "on url:", url)

    return "get_metrics: Metrics collected successfully"


@shared_task()
def send_email_task(from_email, to_email, title, text):
    send_mail(title, text, from_email, [to_email])

    return "send_email_task: mail send successfully"
