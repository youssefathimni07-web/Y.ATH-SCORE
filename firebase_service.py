import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, messaging

firebase_initialized = False

firebase_key = os.getenv("FIREBASE_KEY")

if firebase_key:
    try:
        cred_dict = json.loads(firebase_key)

        cred = credentials.Certificate(cred_dict)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        firebase_initialized = True

    except Exception as e:
        logging.error(f"Firebase init error: {e}")
else:
    logging.warning("FIREBASE_KEY not found → Firebase disabled")


# 🔔 إرسال إشعار (لن يكسر التطبيق)
def send_notification(token: str, title: str, body: str):
    if not firebase_initialized:
        return

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token
        )

        messaging.send(message)

    except Exception as e:
        logging.error(f"Notification error: {e}")
