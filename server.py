from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import time
import threading

app = FastAPI()
clients: Dict[str, Dict] = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients[client_id] = {"ws": websocket, "last_seen": time.time()}
    print(f"{client_id} connecté")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Reçu de {client_id}: {data}")
            clients[client_id]["last_seen"] = time.time()
    except WebSocketDisconnect:
        print(f"{client_id} déconnecté")
        clients.pop(client_id, None)

# Thread de monitoring inactivité
def monitor_clients():
    while True:
        now = time.time()
        for client_id, info in list(clients.items()):
            if now - info["last_seen"] > 30:
                print(f"{client_id} est inactif depuis plus de 30s")
        time.sleep(10)

threading.Thread(target=monitor_clients, daemon=True).start()
