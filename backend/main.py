from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, asyncio
from socket_manager import sio
from firebase_service import send_notification
from ml_model import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "YOUR_API_KEY"

user_tokens = []

@app.post("/save-token")
def save_token(data: dict):
    token = data["token"]
    if token not in user_tokens:
        user_tokens.append(token)
    return {"ok": True}

@app.get("/predict/{h}/{a}")
def predict_api(h: int, a: int):
    return {"result": predict(h, a)}

@app.get("/matches")
def matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_KEY}
    return requests.get(url, headers=headers).json()

# 🔔 إشعار هدف
def notify_goal(name):
    for t in user_tokens:
        send_notification(t, "⚽ هدف!", f"{name} سجل هدف")

last_events = []

def detect_goals(events):
    global last_events

    new = [e for e in events if e not in last_events and e["type"]=="Goal"]

    for g in new:
        notify_goal(g["player"]["name"])

    last_events = events

# 🔴 بث مباشر
async def loop():
    while True:
        data = matches()
        fixtures = data.get("response", [])

        for f in fixtures:
            detect_goals(f.get("events", []))

        await sio.emit("live", data)
        await asyncio.sleep(10)

@app.on_event("startup")
async def start():
    asyncio.create_task(loop())