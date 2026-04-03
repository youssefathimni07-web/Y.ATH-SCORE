import firebase_admin
from firebase_admin import credentials, messaging
import os, json

cred_dict = json.loads(os.environ["FIREBASE_KEY"])
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

def send_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    messaging.send(message)
