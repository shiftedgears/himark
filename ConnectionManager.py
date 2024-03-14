from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import Room
import Client


class ConnectionManager:

    def __init__(self):
        self.active_conn = []

    async def connect(self, client: Client):
        await client.get_socket().accept()
        self.active_conn.append(client)
        print("[WS] Connection Accepted")

    async def broadcast(self, room: Room, message: str):
        print("[WS] Broadcasting to Clients...", end="")
        for client in room.get_client_list():
            await client.websock.send_text(message)
        print("Done.")

    async def send_msg(self, client: Client, message: str):
        await client.websock.send_text(message)
        print("[WS] Message sent to Client")

    def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("[WS] Client disconnected")
