from audioop import add
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConnectionManager import ConnectionManager, Client
from RoomManager import Room, RoomManager
import asyncio
import websockets

app = FastAPI()

# BEGINNING OF MACROS TO BE USED

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"
SERVER_INIT_CONNECTION_RESPONSE_BAD = "DONTTOUCHME"

LIST_SERVER_ROOMS = r"\l"
CHANGE_NAME = r"\n"
CHANGE_ROOM = r"\r"
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
            #interpret the message and handle it if it's a command
            await interpret_message(new_client, data)
    except WebSocketDisconnect:
        conn_manager.disconnect(new_client)


@app.get("/")
def read_root():
    return {"hi": "mark"}


@app.post("/connection_attempt", response_model=client_connection_response)
async def connection_request(request: client_connection_request):  # receive a connection request from the client
    if request.arg1 == CLIENT_INIT_CONNECTION_MESSAGE:
        return client_connection_response(arg2=SERVER_INIT_CONNECTION_RESPONSE)
    else:
        return client_connection_response(arg2=SERVER_INIT_CONNECTION_RESPONSE_BAD)

#interpret and handles a message from the client
async def interpret_message(client: Client, message: str):
    #we want to parse the message to see if there is a command the user is issuing
    if(message.startswith(LIST_SERVER_ROOMS)): #if the request from the user is to list rooms
        room_manager.list_rooms() #this will list the rooms in this room manager
        
    elif(message.startswith(CHANGE_NAME)): #if user wants to change their name 
        args = message.split() #split the message into a list
        #args[0] is CHANGE_NAME
        #args[1] is the new name. anything after the name is not considered part of the name
        try:
            if args[1]: #if there was a second argument
                pass #TODO change the name
        except IndexError:
            pass #TODO not enough arguments provided. tell user
    
    elif(message.startswith(CHANGE_ROOM)): #if client wants to change what room they're in
        args = message.split() #split the message into a list
        #args[0] is CHANGE_ROOM
        #args[1] is the room
        try:
            if args[1]: #if there was a second argument
                if not room_manager.find_room(args[1]): #if a room of name args[1] exists
                    pass #TODO change the room the user is in
                else:
                    pass #TODO tell the user that room doesn't exist
                pass #TODO verify the room exists and change the clients current room
        except IndexError:
            pass #TODO not enough arguments provided. tell user
    
    else:
        #otherwise this is a regular message
        #call function that sends the message to the room the user is in
        await conn_manager.broadcast(f"msg: {message}")
        
