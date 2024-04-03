from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import Room
import Client
import RoomManager

app = FastAPI()

class ConnectionManager:

    def __init__(self):
        self.active_conn = []

    async def connect(self, client: Client):
        await client.get_socket().accept()
        self.active_conn.append(client)
        print("[WS] Connection Accepted")
        
    async def data_connect(self, ws : WebSocket):
        await ws.accept()
        print("[WS] Data Connection Accepted")

    async def broadcast(self, room: Room, message: str):
        print("[WS] Broadcasting to Clients...", end="")
        for client in room.get_client_list():
            await client.websock.send_text(message)
        print("Done.")

    async def send_msg(self, client: Client, message: str):
        await client.websock.send_text(message)
        print(f"[WS] Message sent to Client: {message}")
        
    def active_clients(self) -> list:
        return self.active_conn

    #working on
    def find_client_by_id(self, user_id: str):
        for client in self.active_conn:
            if client.id == user_id:
                return RoomManager.find_client_room(client.name)
        return None

    async def send_room_info(self, user_id: str):
        client = self.find_client_by_id(user_id)
        if client:
            room = RoomManager.find_client_room(client)
            if room:
                room_name = room.get_name()
                await self.send_msg(client, f"You are currently in room: {room_name}")
            else:
                await self.send_msg(client, "You are not in any room.")
        else:
            print(f"[WS] Client not found for user ID: {user_id}")
        #end of working on

    def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("[WS] Client disconnected")

#working on
@app.websocket("/ws_info")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = Client(websocket)
    await ConnectionManager.connect(client)

@app.post("/get_room_info/{user_id}")
async def get_room_info(user_id: str):
    await ConnectionManager.send_room_info(user_id)