from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import Room
import Client

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

class ConnectionManager:

    def __init__(self):
        self.active_conn = []

    async def connect(self, client: Client):
        await client.get_socket().accept()
        self.active_conn.append(client)
        print("[WS] Connection Accepted")
        
    async def data_connect(self, ws : WebSocket):
        await ws.accept()
        print("[WS] Data Connection Accepted")

    async def info_connect(self, ws : WebSocket):
        await ws.accept()
        print("[WS] Info Connection Accepted")

    async def broadcast(self, room: Room, message: str):
        print("[WS] Broadcasting to Clients...", end="")
        for client in room.get_client_list():
            await client.websock.send_text(message)
        print("Done.")

    async def send_msg(self, client: Client, message: str):
        await client.websock.send_text(message)
        print(f"[WS] Message sent to Client: {message}")
        
    def active_clients(self) -> list:
        return self.active_conn

    def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("[WS] Client disconnected")
