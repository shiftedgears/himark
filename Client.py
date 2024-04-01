from fastapi import WebSocket


class Client:
    def __init__(self, websocket: WebSocket, name: str, iden: str):
        self.websock = websocket
        self.name = name
        self.iden = iden
        self.data_websock = None

    def connect(self, addr: str) -> bool:
        pass

    def get_socket(self) -> WebSocket:
        return self.websock

    def set_name(self, name):
        self.name = name

    def set_data_websock(self, data_websock):
        self.data_websock = data_websock

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.iden

    def __repr__(self):
        return f"{self.name}, {self.iden}"

    def __eq__(self, other):
        if self is other:
            return True
        else:
            return False



