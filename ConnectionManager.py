from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class Client:
    def __init__(self, websocket: WebSocket):
        self.websock = websocket

    def connect(self, addr: str) -> bool:
        pass

    def get_socket(self) -> WebSocket:
        return self.websock


class ConnectionManager:
    def __init__(self):
        self.active_conn = []

    async def connect(self, client: Client):
        await client.get_socket().accept()
        self.active_conn.append(client)
        print("[WS] Connection Accepted")

    async def broadcast(self, message: str):
        print("[WS] Broadcasting to Clients...", end="")
        for client in self.active_conn:
            await client.websock.send_text(message)
        print("Done.")

    async def send_msg(self, client: Client, message: str):
        await client.websock.send_text(message)
        print("[WS] Message sent to Client")

    def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("[WS] Client disconnected")
