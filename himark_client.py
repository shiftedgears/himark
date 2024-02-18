import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
import asyncio
from websockets.sync.client import connect
from websockets import WebSocketException
import sys

ip = "127.0.0.1"
port = "8000"

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"

WS_SERVER_ADDR = "ws://127.0.0.1:8000/ws_connect"

if __name__ == "__main__":

    try:
        with connect(WS_SERVER_ADDR) as websocket:
            websocket.send("hello")

            while True:
                recv = websocket.recv()
                print(f"receieved: {recv}")

                txt = input("please enter some text")

                if txt == "exit":
                    websocket.close()
                    exit(0)
                else:
                    websocket.send(txt)

    except WebSocketException as exception:
        print(exception)
