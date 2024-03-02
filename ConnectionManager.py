from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uuid
from RoomManager import Room

class Client:
    def __init__(self, websocket: WebSocket, name: str, user_id: uuid):
        self.websock = websocket
        self.name = name
        self.id = user_id
        self.curr_room = None

    def __str__(self):
        return f"Name: {self.name}, ID: {self.id}, Room: {self.curr_room}"

    async def disconnect(self):
        await self.websock.close()

    def get_socket(self) -> WebSocket:
        return self.websock

    def get_name(self) -> str:
        return self.name

    def get_room(self) -> Room:
        return self.curr_room

    def set_room(self, room: Room) -> bool:
        self.curr_room = Room

    def set_name(self, name: str):
        self.name = name

    def get_id(self):
        return self.id

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

    async def send_msg(self, client_name: str, message: str) -> bool:

        for client in self.active_conn:
            if client_name is client.name:
                await client.websock.send_text(message)
                print("[WS] Message sent to Client")
                return True

        return False

    async def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("[WS] Client disconnected")

    def find_user_by_id(self, user_uuid: uuid) -> Client:
        for user in self.active_conn:
            if user.get_id == user_uuid:
                return user

        return None
