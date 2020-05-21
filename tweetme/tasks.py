from celery import shared_task
from django.core.mail import BadHeaderError, send_mail

from tweetme.settings import DEFAULT_FROM_EMAIL


@shared_task
def contact_mail(data):
    subject = data['subject']
    from_email = data['email']
    to_email = DEFAULT_FROM_EMAIL
    message = data['message']
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [to_email])
        except BadHeaderError:
            pass
    return None
