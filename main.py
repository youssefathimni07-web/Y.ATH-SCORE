from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import asyncio
import logging

from socket_manager import sio
from firebase_service import send_notification
from ml_model import predict

app = FastAPI()

# ----------------- CORS -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- CONFIG -----------------
API_KEY = "4eb6e0ffbcbde3b079c5227e9b9676b8"

user_tokens = []

# 🔥 نظام الإعلانات (Ad Tracking)
ad_clicks = 0
ad_views = 0

# ----------------- SAVE TOKEN -----------------
@app.post("/save-token")
async def save_token(request: Request):
    data = await request.json()
    token = data.get("token")

    if token and token not in user_tokens:
        user_tokens.append(token)

    return {"status": "saved"}

# ----------------- PREDICTION -----------------
@app.get("/predict/{home}/{away}")
def predict_api(home: int, away: int):
    try:
        result = predict(home, away)
        return {"prediction": result}
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return {"error": "prediction failed"}

# ----------------- MATCHES -----------------
@app.get("/matches")
def get_matches():
    try:
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {"x-apisports-key": API_KEY}

        response = requests.get(url, headers=headers, timeout=10)
        return response.json()

    except Exception as e:
        logging.error(f"API error: {e}")
        return {"error": "API failed"}

# ----------------- ADS SYSTEM -----------------
@app.post("/ad-click")
async def ad_click():
    global ad_clicks
    ad_clicks += 1

    return {"clicks": ad_clicks}

@app.post("/ad-view")
async def ad_view():
    global ad_views
    ad_views += 1

    return {"views": ad_views}

@app.get("/ads-stats")
def ads_stats():
    return {
        "views": ad_views,
        "clicks": ad_clicks
    }

# ----------------- NOTIFICATIONS -----------------
def notify_goal(player_name: str):
    for token in user_tokens:
        try:
            send_notification(token, "⚽ Goal!", f"{player_name} scored!")
        except Exception as e:
            logging.error(f"Notification error: {e}")

# ----------------- GOAL DETECTOR -----------------
last_events = []

def detect_goals(events):
    global last_events

    try:
        new_goals = [
            e for e in events
            if e not in last_events and e.get("type") == "Goal"
        ]

        for goal in new_goals:
            player = goal.get("player", {}).get("name", "Player")
            notify_goal(player)

        last_events = events

    except Exception as e:
        logging.error(f"Goal detection error: {e}")

# ----------------- LIVE LOOP -----------------
async def live_loop():
    while True:
        try:
            data = get_matches()
            matches = data.get("response", [])

            for match in matches:
                events = match.get("events", [])
                detect_goals(events)

            await sio.emit("live", data)

        except Exception as e:
            logging.error(f"Live loop error: {e}")

        await asyncio.sleep(10)

# ----------------- STARTUP -----------------
@app.on_event("startup")
async def startup():
    asyncio.create_task(live_loop())
