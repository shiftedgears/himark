from audioop import add
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConnectionManager import ConnectionManager, Client
from RoomManager import Room, RoomManager
import asyncio

app = FastAPI()

# BEGINNING OF MACROS TO BE USED

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"
SERVER_INIT_CONNECTION_RESPONSE_BAD = "DONTTOUCHME"


# ENDING OF MACROS


# CLASSES

class client_connection_request(BaseModel):
    arg1: str


class client_connection_response(BaseModel):
    arg2: str

# END CLASSES


conn_manager = ConnectionManager()
room_manager = RoomManager()

# FastAPI stuff

#Executes before server startup
@app.on_event("startup")
async def start_up():
    try:
        #open rooms txt file
        file = open("rooms.txt", "r")
    #if rooms.txt DNE or not in right directory
    except FileNotFoundError:
        print("Error: rooms.txt not found, creating default room")
        room_manager.add_room('default')
        print("Building rooms...:")
        for room in room_manager.rooms:
            print(room.name)
        return

    while True:
        #read in each room name 
        content = file.readline().strip().replace(' ', '_')
        #if file done, break out 
        if not content:
            break
        #create rooms
        room_manager.add_room(content)
    file.close()
    
    #rooms being built
    print("Building rooms...:")
    for room in room_manager.rooms:
        print(room.name)


@app.websocket("/ws_connect")
async def establish_listener(websocket: WebSocket):

    new_client = Client(websocket)
    await conn_manager.connect(new_client)
    try:
        while True:
            data = await new_client.get_socket().receive_text()
            print(f"From {websocket}")
            await conn_manager.broadcast(f"broadcast msg: {data}")
    except WebSocketDisconnect:
        conn_manager.disconnect(new_client)


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
