import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, messaging

# 🔥 قراءة المفتاح من Environment (آمن)
firebase_key = os.getenv("FIREBASE_KEY")

# ❗ التحقق من وجود المفتاح
if not firebase_key:
    logging.error("FIREBASE_KEY is missing in environment variables")
    raise Exception("FIREBASE_KEY not set")

# تحويل JSON إلى dict
cred_dict = json.loads(firebase_key)

# تهيئة Firebase
try:
    cred = credentials.Certificate(cred_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

except Exception as e:
    logging.error(f"Firebase init error: {e}")
    raise


# 🔔 إرسال إشعار
def send_notification(token: str, title: str, body: str):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token
        )

        response = messaging.send(message)
        return response

    except Exception as e:
        logging.error(f"Send notification error: {e}")
        return None
