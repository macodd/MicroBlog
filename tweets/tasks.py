from celery import shared_task
from django.core.mail import EmailMessage
from render_block import render_block_to_string

from tweetme.settings import DEFAULT_FROM_EMAIL


@shared_task
def mentioned_tweet_mail(email, tweet_id):
    subject = 'Alguien esta hablando de ti!'
    from_email = DEFAULT_FROM_EMAIL
    to_email = email
    html_content = render_block_to_string(
        'emails/mentioned.html',
        'html_main',
        {'tweet_id': tweet_id}
    )

    msg = EmailMessage(
        subject, html_content, from_email, [to_email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
    except:
        print('Unable to send')
        pass
    return None
