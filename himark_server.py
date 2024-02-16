from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class client_request(BaseModel):
    arg1: str

class client_response(BaseModel):
    arg2: str

@app.get("/")
def read_root():
    return {"hi":"mark"}

@app.post("/connecting", response_model=client_response)
def receive(request: client_request):
    print(f"Got {request}")
    return client_response(arg2 = "a response")

@app.get("/BBS")
def display_board_info():
    return {"Channel Title": "Board 1", "Update":"asdfasdfasdf asdfasdfasdfasdf asdfasdfasdfasdfasdf"}
