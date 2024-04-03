from ast import parse
import re
import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException
import sys
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, ListView, ListItem, Header

import json


ip = "127.0.0.1"
port = "8000"

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"

WS_SERVER_ADDR = f"ws://{ip}:{port}/ws_connect"
WS_GET_ROOM_SERVER_ADD = f"ws://{ip}:{port}/client_room"
WS_GET_ROOM_USER_LIST = f"ws://{ip}:{port}/ws_user_list"
WS_INFO_ADDR = f"ws://{ip}:{port}/ws_info"
CONNECT_SERVER_ADDR = f"http://{ip}:{port}/connection_attempt"



class Client_Connection:

    def __init__(self, textual_obj):
        #attempt connection. if it works, continue. otherwise sys exit
        response = requests.post(CONNECT_SERVER_ADDR, json={"arg1":CLIENT_INIT_CONNECTION_MESSAGE})

        if(response.json() != {'arg1':SERVER_INIT_CONNECTION_RESPONSE}):
            sys.exit(f"There is no himark server running on {ip}:{port}")

        self.ws = 0
        self.ws_list = 0
        self.textual_obj = textual_obj

        self.ws_info = 0

        self.id = str()

    #send json to server
    #currenly same port as old one, potentially change
    async def connect_to_ws_info(self):
        try:
            async with websockets.connect(WS_INFO_ADDR) as self.ws_info:
                #Once connected, send the user ID and request
                user_id = self.id 
                message = json.dumps({"user_id": user_id})
                await self.ws.send(message)
                print(f"Sent message: {message}")

                # Wait for messages from the WebSocket server
                await self.wait_for_messages()
        except websockets.exceptions.InvalidURI:
            sys.exit(f"Invalid URI: {WS_INFO_ADDR}")
        except websockets.exceptions.WebSocketException:
            sys.exit("WebSocket error occurred")

    async def wait_for_messages(self):
        try:
            self.id = await self.ws.recv()

            while True:
                recv = await self.ws.recv() #wait for a message
                self.textual_obj.query_one('#message_box').append(ListItem(Label(recv)))
        except WebSocketException:
            sys.exit("WebSocket error occured")
        except asyncio.CancelledError:
            sys.exit("User cancelled")

    async def send_message(self, txt):
        if txt == "exit": #tell the server we are disconnecting
            raise ConnectionClosed
        else:
            await self.ws.send(txt)
            
    async def update_user_list(self):
        try:
            while True:
                recv = await self.ws_list.recv() #wait for a message

                self.textual_obj.query_one('#message_box').append(ListItem(Label(recv)))
        except WebSocketException:
            sys.exit("WebSocket error occured")
        except asyncio.CancelledError:
            sys.exit("User cancelled")


    async def main(self):
        async with websockets.connect(WS_SERVER_ADDR) as self.ws:
            await asyncio.create_task(self.wait_for_messages()) #task for waiting for messages
            async with websockets.connect(WS_GET_ROOM_USER_LIST) as self.ws_list:
                await asyncio.create_task(self.update_user_list())


class Client(App):
    CSS_PATH = "client.tcss"
    LOG_FILE = ".himark.log"
    TITLE = "himark"

    @on(Input.Submitted)
    async def client_input(self) -> None:
        input = self.query_one(Input) #get the input

        try:
            await self.c_conn.send_message(input.value) #send message function from client connection
        except:
            sys.exit("Connection Closed by user")

        input.value = "" #clear input

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(classes="box", id="message_box") #box to put messages in
        yield ListView(classes="names", id="name_box") #box to put connected users in
        yield Input(placeholder=">", type="text") #box to capture input. on submit we call send_message

        try:
            self.c_conn = Client_Connection(self)
            asyncio.create_task(self.c_conn.main()) #run the main function of the client connection
        except WebSocketException:
            #raised when user types 'exit' to quit program
            sys.exit()
        except ConnectionClosed:
            sys.exit("Connection closed")
        except ConnectionError:
            sys.exit(f"No service is running on {ip}:{port}")
        except KeyboardInterrupt:
            sys.exit("Program killed by user")
        except SystemExit:
            sys.exit("Program killed by user")
        except asyncio.CancelledError:
            sys.exit("There was an error cancelling an asynchronous routine")

if __name__ == "__main__":
    client = Client()
    client.run()
