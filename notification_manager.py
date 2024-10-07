from twilio.rest import Client
import os

FROM_NUMBER = os.environ['FROM_NUM']
TO_NUMBER = os.environ['TO_NUM']

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self,price,from_code,to_code,depart_date,return_date):
        self.price = price
        self.from_code = from_code
        self.to_code = to_code
        self.depart_date = depart_date
        self.return_date = return_date

    def send_sms(self):

        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_AUTH']
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=FROM_NUMBER,
            to=TO_NUMBER,
            body=f"Low Price Alert! Only {self.price} to fly from {self.from_code} EUR to {self.to_code}on {self.depart_date} to {self.return_date}."
        )
        print(message.sid)