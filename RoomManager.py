from Client import Client
from Room import Room, RoomObserver

class RoomManager(RoomObserver):

    def __init__(self):
        RoomObserver.__init__(self)
        self.rooms = []
        
    # when called, prints out a list of all the rooms in the room manager
    def list_rooms(self) -> None:
        for room in self.rooms:
            print(f"-{room.name}")

    # find_room(name: str)
    # attempts to return a reference to a room object whose name matches
    # room_name
    # returns a Room on success, None on failure.
    def find_room(self, room_name: str) -> Room:
        for room in self.rooms:
            if room.name == room_name:
                return room

        return None

    # destroy_room(room_name: str)
    # attempts to delete a room that's name matches room_name
    # returns true on success, false on failure
    def destroy_room(self, room_name: str) -> bool:
        for room in self.rooms:
            if room.name == room_name:
                self.rooms.remove(room_name)
                self.detach(room_name)
                return True

        return False

    # add_room(room_name: str)
    # attempts to add a new room to the rooms list
    # returns true on success, false on failure
    # when we add a room, attach an observer to that room
    def add_room(self, room_name: str) -> bool:
        if self.find_room(room_name):
            print(f"Error: Room '{room_name}' already Exists")
            return False
        else:
            self.rooms.append(Room(room_name))
            self.attach(Room(room_name))
            return True

    # add_client(client_name: str, room_name: str)
    # attempts to append a user to a room.
    # returns true on success, or false on failure
    # when we add a client to this room, notify the observer
    async def add_client(self, client: Client, room_name: str) -> bool:
        room = self.find_room(room_name)
        if room is None:
            print("cannot find room")
            return False

        if client not in room.clients:
            room.clients.append(client)
            await self.notify(room_name) #notify the clients of this room via RoomObserver
            return True
        else:
            return False

    # remove_client(name: str, room_name: str)
    # removes a client from the server.
    # Returns true on success, otherwise false.
    # when we remove a client from this room, notify the observer
    async def remove_client(self, client: Client) -> bool:
        room = self.find_client_room(client)
        if room is None:
            return False
        else:
            room.remove_client(client)
            await self.notify(room.name) #notify the clients of this room via RoomObserver
            return True

    # find_client_room(client_name: str)
    # attempts to find a room with client_name as a user.
    # Returns a Room on success, None on failure
    def find_client_room(self, client: Client) -> Room:
        for room in self.rooms:
            for c in room.clients:
                if client.iden == c.iden:
                    return room

        return None

    # find_client(client_name: str)
    # searches through all rooms to see if a user matches client_name
    # Returns true on success, or false on failure
    def find_client(self, client_name) -> bool:
        for room in self.rooms:
            if client_name in room.get_client_list():
                return True

        return False

    # get_rooms()
    # returns a formatted string with all rooms
    def get_rooms(self):
        room_list = str()
        for room in self.rooms:
            room_list = room_list + room.get_name()

        return room_list
