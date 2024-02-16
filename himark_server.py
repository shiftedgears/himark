from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

"""BEGINNING OF MACROS TO BE USED"""

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"
SERVER_INIT_CONNECTION_RESPONSE_BAD = "DONTTOUCHME"

""" ENDING OF MARCORS """

class client_connection_request(BaseModel):
    arg1: str

class client_connection_response(BaseModel):
    arg2: str

@app.get("/")
def read_root():
    return {"hi":"mark"}

@app.post("/connection_attempt", response_model=client_connection_response)
def connection_request(request: client_connection_request): #receive a connection request from the client
    if(request.arg1 == CLIENT_INIT_CONNECTION_MESSAGE):
        return client_connection_response(arg2 = SERVER_INIT_CONNECTION_RESPONSE)
    else:
        return client_connection_response(arg2 = SERVER_INIT_CONNECTION_RESPONSE_BAD)
        
@app.get("/BBS")
def display_board_info():
    return {"Channel Title": "Board 1", "Update":"asdfasdfasdf asdfasdfasdfasdf asdfasdfasdfasdfasdf"}
