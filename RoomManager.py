
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

    def find_room(self, name: str) -> Room:
        for room in self.rooms:
            if room.name == name:
                return room

        return None

    def destroy_room(self, room_name) -> bool:
        for room in self.rooms:
            if room.name == room_name:
                self.rooms.remove(room_name)
                return True

        return False

    def add_room(self, room_name: str) -> bool:
        if self.find_room(room_name):
            print("Error: Room already Exists")
            return False
        else:
            self.rooms.append(Room(room_name))
            return True

    def add_client(self, client_name, room_name) -> bool:
        room = self.find_room(room_name)
        if room is None:
            print("cannot find room")
            return False

        if room.add_client(client_name):
            return True
        else:
            return False

    def remove_client(self, client_name, room_name):
        room = self.find_room(room_name)
        if room is None:
            print("cannot find room")
            return False

        if room.remove_client(client_name):
            return True
        else:
            return False

    def find_client_room(self, client_name) -> Room:
        for room in self.rooms:
            if client_name in room.clients:
                return room

        return None

    def find_client(self, client_name) -> bool:
        for room in self.rooms:
            if client_name in room.clients:
                return True

        return False
