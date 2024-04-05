from audioop import add
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConnectionManager import ConnectionManager
from Client import Client
from Room import Room
from RoomManager import RoomManager
import uuid
import asyncio
import websockets

app = FastAPI()

# BEGINNING OF MACROS TO BE USED

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"
SERVER_INIT_CONNECTION_RESPONSE_BAD = "DONTTOUCHME"

ROOM_NOT_FOUND = "That room does not exist."
NO_NAME_PROVIDED = r"Please provide a name, i.e. \n BillyBee"
NO_ROOM_PROVIDED = r"Please provide a room name, i.e. \r the_holodeck"

ASK_USERNAME = "Need Username."
ASK_ROOM = "Which Room?\n"

LIST_SERVER_ROOMS = r"\l"
CHANGE_NAME = r"\n"
CHANGE_ROOM = r"\r"
# ENDING OF MACROS


# CLASSES

class client_connection_re(BaseModel):#basic response/request class model
    arg1: str


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
    else:
        while True:
            #read in each room name 
            content = file.readline().strip().replace(' ', '_')
            #if file done, break out 
            if not content:
                break
            #create rooms
            room_manager.add_room(content)
        file.close()
    finally:
        #rooms being built
        print("Building rooms...:")
        for room in room_manager.rooms:
            print(room.name)


@app.websocket("/ws_connect")
async def establish_listener(websocket: WebSocket):

    new_id = uuid.uuid4()
    new_client = Client(websocket, "default", str(new_id))
    name_established = False
    found_room = False
    await conn_manager.connect(new_client)
    try:
        while True:
            if not name_established:
                await conn_manager.send_msg(new_client, str(new_id))
                await conn_manager.send_msg(new_client, ASK_USERNAME)
                user_name = await new_client.get_socket().receive_text()
                new_client.set_name(user_name)
                await conn_manager.send_msg(new_client, f"{ASK_ROOM} {room_manager.get_rooms()}")
                desired_room = await new_client.get_socket().receive_text()
                while not found_room:
                    if room_manager.find_room(desired_room) is None:
                        await conn_manager.send_msg(new_client, ROOM_NOT_FOUND)
                        desired_room = await new_client.get_socket().receive_text()
                    else:
                        await room_manager.add_client(new_client, desired_room)
                        found_room = True
                print(f"New connection!: {new_client}")
                await conn_manager.send_msg(new_client, f"==== JOINED THE ROOM {desired_room} ====")
                name_established = True
            data = await new_client.get_socket().receive_text()
            print(f"From {new_client}")
            # interpret the message and handle it if it's a command
            await interpret_message(new_client, data)
    except WebSocketDisconnect:
        conn_manager.disconnect(new_client)
        await room_manager.remove_client(new_client)

@app.websocket("/ws_user_list")
async def users_in_room(websocket: WebSocket):
    #have a connection for this client that keeps an updated list of users in the room
    #they are currently in
    #when this client connects, we want to associate this new websocket with the existing client
    try:
        await conn_manager.data_connect(websocket) #accept the connection on this data websocket
        #client has accepted the connection. the first message received will be this users ID
        t_uid = await websocket.receive_text()
        
        #get the list of clients
        clients_list = conn_manager.active_clients()
        client = None
        
        for c in clients_list:
            if c.iden == t_uid:
                c.set_data_socket(websocket)
                client = c
                break
            
        if not client: #if we did not find the client with this id
            raise WebSocketDisconnect
        
        #otherwise, c is the client that is connected on websocket and their data socket has been
        #set successfully
        while True:
            d = await client.get_data_socket().receive_text()
            print(f"{d}")
    except WebSocketDisconnect:
        print(f"[WS] DATA - WebSocket Disconnected")

@app.websocket("/ws_info")
async def websocket_info(websocket: WebSocket):
    try:
        await conn_manager.info_connect(websocket)
        user_id = await websocket.receive_text()

        clients_list = conn_manager.active_clients()
        client = None

        for c in clients_list:
            print(f"client ID {c.iden}, given ID {user_id}")
            if c.iden == user_id:
                c.set_info_socket(websocket)
                print("set info socket")
                client = c
                break

        if not client: #if we did not find the client with this id
            raise WebSocketDisconnect

        print(f"client {client} found")

        while True:
            print("wait")
            data = await client.get_info_socket().receive_text()
            print(f"{data}")

    except WebSocketDisconnect:
        print(f"[WS] INFO - WebSocket Disconnected")


@app.post("/connection_attempt", response_model=client_connection_re)
async def connection_request(request: client_connection_re):  # receive a connection request from the client
    if request.arg1 == CLIENT_INIT_CONNECTION_MESSAGE:
        return client_connection_re(arg1=SERVER_INIT_CONNECTION_RESPONSE)
    else:
        return client_connection_re(arg1=SERVER_INIT_CONNECTION_RESPONSE_BAD)

#interpret and handles a message from the client
async def interpret_message(client: Client, message: str):
    #we want to parse the message to see if there is a command the user is issuing
    if(message.lower().startswith(LIST_SERVER_ROOMS)): #if the request from the user is to list rooms
        await conn_manager.send_msg(client, room_manager.get_rooms()) #this will list the rooms in this room manager
        
    elif(message.lower().startswith(CHANGE_NAME)): #if user wants to change their name
        args = message.split() #split the message into a list
        #args[0] is CHANGE_NAME
        #args[1] is the new name. anything after the name is not considered part of the name
        try:
            if args[1]: #if there was a second argument
                client.set_name(args[1])
                await conn_manager.send_msg(client, f"=== CHANGED NAME TO {args[1]} ====")
        except IndexError:
            await conn_manager.send_msg(client, NO_NAME_PROVIDED)
    
    elif(message.lower().startswith(CHANGE_ROOM)): #if client wants to change what room they're in
        args = message.split() #split the message into a list
        #args[0] is CHANGE_ROOM
        #args[1] is the room
        try:
            if args[1]: #if there was a second argument
                if room_manager.find_room(args[1]): #if a room of name args[1] exists
                    await room_manager.remove_client(client)
                    await room_manager.add_client(client, args[1])
                    await conn_manager.send_msg(client, f"==== CHANGE ROOM TO {args[1]} ====")
                else: #no room exists, tell user
                    await conn_manager.send_msg(client, ROOM_NOT_FOUND)
        except IndexError:
            await conn_manager.send_msg(client, NO_ROOM_PROVIDED)
    
    else:
        #otherwise this is a regular message
        #call function that sends the message to the room the user is in
        room = room_manager.find_client_room(client)
        await conn_manager.broadcast(room, f"{client.get_name()}: {message}")
        
