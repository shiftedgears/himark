from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()

# BEGINNING OF MACROS TO BE USED

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"
SERVER_INIT_CONNECTION_RESPONSE_BAD = "DONTTOUCHME"


# ENDING OF MACROS


# CLASSES
class Client:
    def __init__(self, websocket: WebSocket):
        self.websock = None

    def connect(self, addr: str) -> bool:
        pass

    def get_socket(self) -> WebSocket:
        if self.websock is None:
            raise Exception("Socket does not exist")
        else:
            return self.websock

class ConnectionManager:
    def __init__(self):
        self.active_conn = []

    async def connect(self, client: Client):
        await client.get_socket().accept()
        self.active_conn.append(client)
        print("Connection Accepted")

    async def broadcast(self, message: str):
        print("Broadcasting to Clients...")
        for client in self.active_conn:
            await client.websock.send_text(message)
        print("...Done.")

    async def send_msg(self, client: Client, message: str):
        await client.websock.send_text(message)
        print("Message sent to Client")

    def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("Client disconnected")





class client_connection_request(BaseModel):
    arg1: str


class client_connection_response(BaseModel):
    arg2: str

# END CLASSES


manager = ConnectionManager()


# FastAPI stuff

@app.websocket("/ws_connect")
async def establish_listener(websocket: WebSocket):
    new_client = Client(websocket)
    await manager.connect(new_client)
    try:
        while True:
            data = await new_client.get_socket().receive_text()
            print(data)
            await manager.broadcast("oh hai mark")
    except WebSocketDisconnect:
        manager.disconnect(new_client)
        await manager.send_msg(new_client, "goodbye")


@app.get("/")
def read_root():
    return {"hi": "mark"}


@app.post("/connection_attempt", response_model=client_connection_response)
def connection_request(request: client_connection_request):  # receive a connection request from the client
    if request.arg1 == CLIENT_INIT_CONNECTION_MESSAGE:
        return client_connection_response(arg2=SERVER_INIT_CONNECTION_RESPONSE)
    else:
        return client_connection_response(arg2=SERVER_INIT_CONNECTION_RESPONSE_BAD)


@app.get("/BBS")
def display_board_info():
    return {"Channel Title": "Board 1", "Update": "asdfasdfasdf asdfasdfasdfasdf asdfasdfasdfasdfasdf"}
