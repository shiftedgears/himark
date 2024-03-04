# himark

# Overview
Himark is a CLI chat application. Users host a himark.server application on their computer/server. Then using the himark.client application users can supply the IP address of a himark server, connect to a channel on that server with a nickname, and chat/receive messages from that channel. 

# Packages Required

- fastapi
- uvicorn[standard]
- websockets
- requests
- aioconsole
- pydantic
- asyncio

# Running the Server
First, make sure you are in your venv with the required packages from above. 

Then create a .txt file under the name 'rooms.txt' with the names of the rooms you wish to host on the server, in your same directory as himark_server.py. 
The rooms are read in one line at a time and spaces will be turned to underscores to make switching rooms implementation easier.
If rooms.txt cannot open or be found, one default room will be created under the name 'default'.

Next, run \
```uvicorn himark_server:app --reload``` \
in your terminal. This will host the server on your local machine on port 8000.