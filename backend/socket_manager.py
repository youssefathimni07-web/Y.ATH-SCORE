import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print("Connected:", sid)

@sio.event
async def message(sid, data):
    await sio.emit("message", data)