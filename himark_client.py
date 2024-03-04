import requests
from requests.exceptions import ConnectionError
from pydantic import BaseModel
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException
import sys
import aioconsole

ip = "127.0.0.1"
port = "8000"

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"

WS_SERVER_ADDR = f"ws://{ip}:{port}/ws_connect"
CONNECT_SERVER_ADDR = f"http://{ip}:{port}/connection_attempt"

async def wait_for_messages(ws):
    while True:
        recv = await ws.recv() #wait for a message

        print(f"Received: {recv}")

async def send_message(ws):
    usr_exit = True
    try:
        while usr_exit:
            txt = await aioconsole.ainput("please enter some text ")

            if txt == "exit": #tell the server we are disconnecting
                await ws.close()
                usr_exit = False
            else:
                await ws.send(txt)
    except KeyboardInterrupt:
        await ws.close()
        sys.exit("Program killed via Ctrl-c by user")

async def main():
    try:
        #test to see if a himark server is running on the given ip:port
        response = requests.post(CONNECT_SERVER_ADDR, json={"arg1":CLIENT_INIT_CONNECTION_MESSAGE})

        if(response.json() != {'arg2':SERVER_INIT_CONNECTION_RESPONSE}):
            sys.exit(f"There is no himark server running on {ip}:{port}")

        async with websockets.connect(WS_SERVER_ADDR) as websocket:

            message_wait = asyncio.create_task(wait_for_messages(websocket)) #task for waiting for messages
            send_msg = asyncio.create_task(send_message(websocket))

            await message_wait
            await send_msg

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


if __name__ == "__main__":
    asyncio.run(main()) #run the main function asynchronously, so it can await message-wait and send_msg
