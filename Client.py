from fastapi import WebSocket

"""
    himark, the CLI chat application
    Copyright (C) 2024  Curtis Bachen, Nicholas Hopkins, and Vladislav Mazur.

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

class Client:
    def __init__(self, websocket: WebSocket, name: str, iden: str):
        self.websock = websocket
        self.name = name
        self.iden = iden
        self.data_websock = 0
        self.info_websock = 1

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

