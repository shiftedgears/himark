import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException
import sys
import aioconsole
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, ListView, ListItem

ip = "127.0.0.1"
port = "8000"

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"

WS_SERVER_ADDR = f"ws://{ip}:{port}/ws_connect"
CONNECT_SERVER_ADDR = f"http://{ip}:{port}/connection_attempt"

GLOBAL_WS = None

async def wait_for_messages(textual_obj):
    while True:
        recv = await GLOBAL_WS.recv() #wait for a message

        textual_obj.query_one('#message_box').append(ListItem(Label(recv)))

async def send_message(textual_obj, event):
    txt = textual_obj.query_one(event)

    if txt.value == "exit": #tell the server we are disconnecting
        await GLOBAL_WS.close()
    else:
        await GLOBAL_WS.send(txt.value)



async def main(textual_obj):
    try:
        #test to see if a himark server is running on the given ip:port
        response = requests.post(CONNECT_SERVER_ADDR, json={"arg1":CLIENT_INIT_CONNECTION_MESSAGE})

        if(response.json() != {'arg2':SERVER_INIT_CONNECTION_RESPONSE}):
            sys.exit(f"There is no himark server running on {ip}:{port}")

        async with websockets.connect(WS_SERVER_ADDR) as websocket:

            GLOBAL_WS = websocket

            asyncio.create_task(wait_for_messages(textual_obj)) #task for waiting for messages

    except WebSocketException:
        #raised when user types 'exit' to quit program
        sys.exit(1)
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


class Client(App):
    CSS_PATH = "client.tcss"

    @on(Input.Submitted)
    async def on_input_submitted(self) -> None:
        send_message(self, Input)

    def compose(self) -> ComposeResult:
        yield ListView(classes="box", id="message_box") #box to put messages in
        yield ListView(classes="names", id="name_box") #box to put connected users in
        yield Input(placeholder=">", type="text") #box to capture input. on submit we call  send_message

        asyncio.create_task(main(self))

if __name__ == "__main__":
    client = Client()
    client.run()
