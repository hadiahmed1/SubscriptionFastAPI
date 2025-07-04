from email.mime.text import MIMEText
import smtplib
from config import GMAIL_ID, GMAIL_PASSWORD

# print("START")
# creates SMTP session
s = smtplib.SMTP("smtp.gmail.com", 587)
# # start TLS for security
# s.starttls()
# # Authentication
# s.login(GMAIL_ID, GMAIL_PASSWORD)
# # message to be sent
# message = "Message_you_need_to_send"
# # sending the mail
# s.sendmail(GMAIL_ID, "969hadiahmed@gmail.com", message)
# # terminating the session
# s.quit()
# print("DONE")


def send_email(text, subject, sendTo):
    print("START")
    message = MIMEText(text, "plain")
    message["Subject"] = subject
    message["From"] = GMAIL_ID
    message["To"] = sendTo

    s.starttls()  # Secure the connection
    s.login(GMAIL_ID, GMAIL_PASSWORD)
    s.sendmail(GMAIL_ID, sendTo, message.as_string())
    s.quit()
    print("Sent")
