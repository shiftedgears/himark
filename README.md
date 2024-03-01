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
First, make sure you are in your venv with the required packages from above. Next, run \
```uvicorn himark_server:app --reload``` \
in your terminal. This will host the server on your local machine on port 8000.
