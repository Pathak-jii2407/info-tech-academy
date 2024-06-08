# import smtplib



from django.core.mail import send_mail
from django.conf import settings

def send(user_email, first_name):
    subject = 'Welcome to Our Site'
    message = f'Hi {first_name},\n\nThank you for signing up. Please click the following link to sign in:\n http://127.0.0.1:8000/student-account'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list)
    

# import smtplib,ssl
# smtp_server = 'smtp.gmail.com'
# port = 465

# sender = 'ved24072003@gmail.com'
# password = input('Enter password:')

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
#     server.login(sender,password)