import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self,email, price,from_code,to_code,depart_date,return_date):
        self.email = email
        self.price = price
        self.from_code = from_code
        self.to_code = to_code
        self.depart_date = depart_date
        self.return_date = return_date

    def send_email(self):

        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = os.environ["MY_EMAIL"]
        password = os.environ["MY_PASSWORD"]


        receiver_email = self.email
        subject = "Exclusive Flight Deals for You!"
        body = f"Low Price Alert! Only {self.price} to fly from {self.from_code} EUR to {self.to_code} on {self.depart_date} to {self.return_date}."

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()


