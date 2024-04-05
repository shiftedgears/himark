from fastapi import WebSocket


class Client:
    def __init__(self, websocket: WebSocket, name: str, iden: str):
        self.websock = websocket
        self.name = name
        self.iden = iden
        self.data_websock = 0
        self.info_websock = 0

    def get_socket(self) -> WebSocket:
        return self.websock

    def set_name(self, name):
        self.name = name

    def set_data_socket(self, data_websock):
        self.data_websock = data_websock

    def get_data_socket(self) -> WebSocket:
        return self.data_websock

    def set_info_socket(self, info_websock: WebSocket):
        self.info_websock = info_websock

    def get_info_socket(self) -> WebSocket:
        return self.info_websock

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

