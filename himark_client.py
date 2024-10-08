import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException
import sys
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, ListView, ListItem, Header, Footer

"""
    himark, the CLI chat application
    Copyright (C) 2024  Curtis Bachen, Nicholas Hopkins, and Vladislav Mazur.

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

ip = "127.0.0.1"
port = "8000"

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"

WS_SERVER_ADDR = f"ws://{ip}:{port}/ws_connect"
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
        self.ws_info = 0
        self.textual_obj = textual_obj
        self.id = -1

    async def wait_for_messages(self):
        async with websockets.connect(WS_SERVER_ADDR) as self.ws:
            try:
                self.id = await self.ws.recv()
                while True:
                    recv = await self.ws.recv() #wait for a message
                    self.textual_obj.query_one('#message_box').append(ListItem(Label(recv)))
            except WebSocketException:
                raise WebSocketException
            except asyncio.CancelledError:
                raise asyncio.CancelledError
            except asyncio.exceptions.CancelledError:
                raise asyncio.exceptions.CancelledError

    async def send_message(self, txt):
        if txt == "exit": #tell the server we are disconnecting
            raise SystemExit
        else:
            await self.ws.send(txt)
            
    async def update_user_list(self):
        async with websockets.connect(WS_GET_ROOM_USER_LIST) as self.ws_list:
            try:
                while self.id == -1: #wait for the id of the user to be set
                    await asyncio.sleep(0.1)
                    
                await self.ws_list.send(self.id) #send the data connection the id of this user
                
                while True:
                    recv = await self.ws_list.recv() #wait for a message (which will be the list of users)
                    self.textual_obj.query_one('#name_box').clear()
                    self.textual_obj.query_one('#name_box').append(ListItem(Label("Names:")))
                    self.textual_obj.query_one('#name_box').append(ListItem(Label(recv)))
            except WebSocketException:
                raise WebSocketException
            except asyncio.CancelledError:
                raise asyncio.CancelledError
            except asyncio.exceptions.CancelledError:
                raise asyncio.exceptions.CancelledError
            except:
                raise SystemExit

    async def connect_to_ws_info(self):
        async with websockets.connect(WS_INFO_ADDR) as self.ws_info:
            try:
                while self.id == -1:
                    await asyncio.sleep(0.1)

                user_id = self.id
                await self.ws_info.send(user_id)

                while True:
                    data = await self.ws_info.recv()
                    self.textual_obj.sub_title = data

            except websockets.exceptions.InvalidURI:
                sys.exit(f"Invalid URI: {WS_INFO_ADDR}")
            except websockets.exceptions.WebSocketException:
                raise websockets.exceptions.WebSocketException
            except asyncio.exceptions.CancelledError:
                raise asyncio.exceptions.CancelledError

    async def main(self):
        try:
            await asyncio.gather(
                self.wait_for_messages(),
                self.update_user_list(),
                self.connect_to_ws_info())
        except asyncio.exceptions.CancelledError:
            raise asyncio.exceptions.CancelledError

class Client(App):
    LOG_FILE = ".himark.log"
    TITLE = "himark"
    SUB_TITLE = ""

    BINDINGS = [("\l", "None", "List Rooms"), (r"\n [NAME]", "NONE", "Change name"), (r"\r [ROOM]", "NONEE", "Change room"), ("CTRL+C" , "NOONE", "Exit program")]

    @on(Input.Submitted)
    async def client_input(self) -> None:
        input = self.query_one(Input) #get the input

        try:
            await self.c_conn.send_message(input.value) #send message function from client connection
        except SystemExit:
            raise SystemExit
        except asyncio.exceptions.CancelledError:
                asyncio.exceptions.CancelledError

        input.value = "" #clear input

    def compose(self) -> ComposeResult:
        self.screen.layout = "grid"
        self.screen.grid_size = 2
        self.screen.grid_columns = "80% 20%"
        self.screen.grid_rows = "80% 20%"

        yield Header()

        self.message_box = ListView(classes="box", id="message_box") #box to put messages in
        yield self.message_box
        self.message_box.styles.height = "90%"
        self.message_box.styles.border = ("solid", "green")
        self.message_box.styles.text_align = "center"

        self.name_box = ListView(classes="names", id="name_box") #box to put connected users in
        yield self.name_box
        self.name_box.styles.dock = "right"
        self.name_box.styles.width = "15%"
        self.name_box.styles.height = "70%"

        yield Input(placeholder=">", type="text") #box to capture input. on submit we call send_message

        yield Footer()

        try:
            self.c_conn = Client_Connection(self)
            asyncio.create_task(self.c_conn.main()) #run the main function of the client connection
        except WebSocketException:
            #raised when user types 'exit' to quit program
            sys.exit("Exit")
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
        except asyncio.exceptions.CancelledError:
            sys.exit("Program killed by user")
        except websockets.exceptions.WebSocketException:
            sys.exit("Websockets exception raised")
        except:
            sys.exit("An unexepected error occurred")

if __name__ == "__main__":
    client = Client()
    client.run()
