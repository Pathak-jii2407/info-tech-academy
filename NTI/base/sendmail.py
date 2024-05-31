# import smtplib


# def send(user_email,first_name,link):
#     sender = "ved24072003@gmail.com"
#     receiver = user_email

#     message = f"""\
#     Subject: Hi Mailtrap
#     To: {receiver}
#     From: NTI-Tech-Academy
#     Hey, {first_name}
#     You have been signup for NTI Tech Academy please clicj the link below\n ."""

#     with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
#         server.starttls()
#         server.login("466d740876e7a0", "7b1692609c78a4")
#         server.sendmail(sender, receiver, message)
#         print('done')


from django.core.mail import send_mail
from django.conf import settings

def send(user_email, first_name):
    subject = 'Welcome to Our Site'
    message = f'Hi {first_name},\n\nThank you for signing up. Please click the following link to sign in:\n http://127.0.0.1:8000/student-account'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list)
