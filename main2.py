import os
from random import random

from fastapi import FastAPI
app = FastAPI()


from signalwire.rest import Client as signalwire_client
#
# class CustomConsumer(Consumer):
#
#     def set_message(self,send_to,send_from,body):
#         self.send_to = send_to
#         self.send_from = send_from
#         self.send_body = body
#
#     def setup(self):
#         self.project = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
#         self.token = 'PTXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
#         self.contexts = ['office']
#
#     def ready(self):
#         self.client.messaging.send(context='office', to_number=self.send_to, from_number=self.send_from, body='Welcome to SignalWire!')
#



@app.get("/signal")
async def signal():
    data = {}
    client = signalwire_client()

    # Generate a randome 6 digit code between 123456 - 987654
    auth_code = str(random.randint(123456, 987654))
    # Get the phone number to challenge from request
    number = '+77054502569'
    # Add the session to the in-memory global request object
    data['requests'].append({
        'number': number,
        'code': auth_code
    })

    # Send a message, with challenge code to phone number provided.
    message = client.messages.create(
        from_='+77472298247',
        body="Your authorization code is: " + auth_code,
        to=number
    )
    # consumer.set_message('+77472298247','+77054502569','Welcome at SignalWire!')

    return "send"

