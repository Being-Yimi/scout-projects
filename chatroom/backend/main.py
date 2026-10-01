from fastapi import FastAPI,  WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import sqlite3
from datetime import datetime

app = FastAPI()

def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_message(sender, content):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender, content, timestamp) VALUES (?, ?, ?)",
        (sender, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_messages(limit=50):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sender, content, timestamp FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"sender": r[0], "content": r[1], "timestamp": r[2]} for r in reversed(rows)]

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    return {"message": "聊天室后端已启动"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    for msg in get_messages():
        await websocket.send_json(msg)
    try:
        while True:
            data = await websocket.receive_json()
            save_message(data["sender"], data["content"])
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)