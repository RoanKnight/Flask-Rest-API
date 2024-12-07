from flask_mail import Message
from flask import current_app
from threading import Thread
from app import mail

# Function to send email asynchronously
def send_async_email(app, msg):
  # Create an application context for the email sending thread
  with app.app_context():
    mail.send(msg)

# Function to send an email, either synchronously or asynchronously
def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
  # Create a new email message object
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body

  # If there are any attachments, add them to the email
  if attachments:
    for attachment in attachments:
      # Attach each file to the email
      msg.attach(*attachment)

  # Check if the email should be sent synchronously
  if sync:
    # Send the email immediately in the current thread
    mail.send(msg)
  else:
    # Send the email asynchronously in a new thread
    Thread(target=send_async_email, args=(
        current_app._get_current_object(), msg)).start()
