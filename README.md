# himark

## Overview
Himark is a CLI chat application. Users host a himark.server application on their home computer/server. Then using the himark.client application users can supply the IP address of a himark server, connect to a channel on that server with a nickname, and chat/receive messages from that channel.

## Packages Required

- fastapi
- uvicorn[standard]
- websockets
- requests
- pydantic
- asyncio
- textual

## Both Client & Server
### Virtual Environment Setup
If you are running the server in a virtual environment, use the command\
```python3 -m venv ./himark_venv ```\
to create your virtual environment, and then change into your virtual environment via\
```source ./himark_venv/bin/activate ```

## Running the Server
### rooms.txt
Create a .txt file under the name 'rooms.txt' with the names of the rooms you wish to host on the server, in the same directory as himark_server.py. 
The rooms are read in one line at a time and spaces will be turned to underscores to make switching rooms implementation easier.
If rooms.txt cannot open or be found, one default room will be created under the name 'default'.

### Commands for Running the Server
Once in your venv, or if you choose not to have a virtual environment, ensure you have the required packages by running\
```pip install -r requirements.txt```\
which will install the needed packages.

Once finished you can start the server by running \
```uvicorn himark_server:app --reload``` \
in your terminal while in the directory with himark_server.py. This will host the server on your local machine on port 8000.

## Client
### Commands for Connecting to a Server
Once in your venv, or if you choose not to have a virutal environment, ensure you have the required packages by running\
```pip install -r requirements.txt ```\
which will install the needed packages.

Once finished you can connect to a server by running himark_client.py \\\
```python himark_client.py````\
which will connect you to a himark server running on your local machine on port 8000.
