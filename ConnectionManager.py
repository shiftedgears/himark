from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class Client:
    def __init__(self, websocket: WebSocket, name: str, id: str):
        self.websock = websocket
        self.name = name
        self.id = id

    def connect(self, addr: str) -> bool:
        pass

    def disconnect(self):
        self.websock.close()

    def get_socket(self) -> WebSocket:
        return self.websock

    def get_name(self) -> str:
        return self.name


class ConnectionManager:
    def __init__(self):
        self.active_conn = []

    async def connect(self, client: Client):
        await client.get_socket().accept()
        self.active_conn.append(client)
        print("[WS] Connection Accepted")

    async def broadcast(self, message: str):
        print("[WS] Broadcasting to Clients...", end="")
        for client in self.active_conn:
            await client.websock.send_text(message)
        print("Done.")

    async def send_msg(self, client_name: str, message: str) -> bool:

        for client in self.active_conn:
            if client_name is client.name:
                await client.websock.send_text(message)
                print("[WS] Message sent to Client")
                return True

        return False

    def disconnect(self, client: Client):
        self.active_conn.remove(client)
        print("[WS] Client disconnected")

    #function to tell this specific client a message
    async def tell_client(self, client: Client, message: str):
        await client.websock.send_text(message)
