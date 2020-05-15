from django.core.mail import EmailMessage
from render_block import render_block_to_string


def mentioned_tweet_mail(email, tweet_id):
    subject = 'Alguien esta hablando de ti!'
    from_email = 'no-reply@fogata.com'
    to_email = email
    html_content = render_block_to_string(
        'emails/mentioned.html',
        {'tweet_id': tweet_id}
    )

    msg = EmailMessage(
        subject, html_content, from_email, [to_email],
    )
    msg.content_subtype = "html"
    msg.send()
