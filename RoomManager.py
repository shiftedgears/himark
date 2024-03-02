
class Room:
    def __init__(self, name: str = "default"):
        self.name = name
        self.clients = []

    def add_client(self, name: str) -> bool:
        if name not in self.clients:
            self.clients.append(name)
            return True
        else:
            print("User already in List")
            return False

    def remove_client(self, name: str) -> bool:
        if name in self.clients:
            self.clients.remove(name)
            return True
        else:
            print("No user found")
            return False

    def clear(self):
        self.clients.clear()

    def get_name(self):
        return self.name


class RoomManager:
    def __init__(self):
        self.rooms = []
        
    #when called, prints out a list of all the rooms in the room manager
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
                return True

        return False

    # add_room(room_name: str)
    # attempts to add a new room to the rooms list
    # returns true on success, false on failure
    def add_room(self, room_name: str) -> bool:
        if self.find_room(room_name):
            print("Error: Room already Exists")
            return False
        else:
            self.rooms.append(Room(room_name))
            return True

    # add_client(client_name: str, room_name: str)
    # attempts to append a user to a room.
    # returns true on success, or false on failure
    def add_client(self, client_name: str, room_name: str) -> bool:
        room = self.find_room(room_name)
        if room is None:
            print("cannot find room")
            return False

        if client_name not in room.clients:
            room.clients.append(client_name)
            return True
        else:
            return False

    # remove_client(name: str, room_name: str)
    # removes a client from the server.
    # Returns true on success, otherwise false.
    def remove_client(self, client_name: str, room_name: str)  -> bool:
        room = self.find_room(room_name)
        if room is None:
            print("cannot find room")
            return False

        if room.remove_client(client_name):
            return True
        else:
            return False

    # find_client_room(client_name: str)
    # attempts to find a room with client_name as a user.
    # Returns a Room on success, None on failure
    def find_client_room(self, client_name: str) -> Room:
        for room in self.rooms:
            if client_name in room.clients:
                return room

        return None

    # find_client(client_name: str)
    # searches through all rooms to see if a user matches client_name
    # Returns true on success, or false on failure
    def find_client(self, client_name) -> bool:
        for room in self.rooms:
            if client_name in room.clients:
                return True

        return False
