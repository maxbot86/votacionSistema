#Lib to Check Emails Alerts/Subscribed
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

#===ENV VARS = ===================
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")

def sendEmail(to_email, subject,body):
    #here we define the logic to send and Email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach Body To Msg
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connecto to SMTP Server
        server = smtplib.SMTP(smtp_server)
        # Send Email
        server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent to  {to_email}")
        result = True
        server.quit()
    except Exception as e:
        print(f"Error: {e}")
        result = False
    return result
