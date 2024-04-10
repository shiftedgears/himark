from Client import Client

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

class Room:
    def __init__(self, name: str = "default"):
        self.name = name
        self.clients = list()

    def get_client_list(self):
        return self.clients

    #return the list of clients as a string deliminated by \n's
    def get_formatted_client_list(self) -> str:
        client_list = str()
        for client in self.clients:
            client_list += client.get_name() + '\n'
        
        return client_list[:-1]

    def add_client(self, client: Client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            return True
        else:
            print("User already in List")
            return False

    def remove_client(self, client: Client) -> bool:
        if client in self.clients:
            self.clients.remove(client)
            return True
        else:
            print("No user found")
            return False

    def clear(self):
        self.clients.clear()

    def get_name(self):
        return self.name

    #on update, tell all connected clients on the ws
    #the newly updated client list for this room object
    async def update(self):
        for client in self.clients: #for every client in this room
            #tell them the new list of clients
            await client.data_websock.send_text(self.get_formatted_client_list())

# https://www.geeksforgeeks.org/observer-method-python-design-patterns/
# https://refactoring.guru/design-patterns/observer/python/example#example-0
class RoomObserver:

    #create an empty list of observers
    def __init__(self):
        self.observers = []

    #on notification (room added/removed a client)
    #loop through all the observers and update them
    #each observer is a room object
    async def notify(self, room: Room):
        for o in self.observers:
            if o.name == room.name: #when we find this room
                await room.update() #call its update function

    # Attach an observer to the RoomObserver
    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        try:
            for o in self.observers:
                if o.room_name == observer:
                    self.observers.remove(o)
        except:
            print("{observer} not in list")
