import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = 'ENTer the password'
SENDER = 'Enter the sender mail id'
RECEVIER = 'ENter the reciver mail id'
def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'New customer Shown up!'
    email_message.set_content('Hey, we just saw a new customer')

    with open(image_path, 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype='image',subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEVIER. email_message.as_string())
    gmail.quit()