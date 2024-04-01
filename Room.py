from Client import Client

# https://www.geeksforgeeks.org/observer-method-python-design-patterns/
# https://refactoring.guru/design-patterns/observer/python/example#example-0
class RoomObserver:

    #create an empty list of observers
    def __init__(self):
        self.observers = []

    #on notification (room added/removed a client)
    #loop through all the observers and update them
    #each observer is a room object
    def notify(self, room_name: list):
        for o in self.observers:
            if o.name == room_name: #when we find this room
                o.update(self) #call its update function

    # Attach an observer to the RoomObserver
    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        try:
            self.observers.remove(observer)
        except:
            print("{observer} not in list")


class Room:
    def __init__(self, name: str = "default"):
        self.name = name
        self.clients = list()

    def get_client_list(self):
        return self.clients

    #return the list of clients as a string deliminated by \n's
    def get_formatted_client_list(self):
        client_list = str()
        for client in self.clients:
            client_list += client.get_name() + '\n'

    def add_client(self, client: Client) -> bool:
        if client not in self.clients:
            self.clients.append(client)
            self.notify()
            return True
        else:
            print("User already in List")
            return False

    def remove_client(self, client: Client) -> bool:
        if client in self.clients:
            self.clients.remove(client)
            self.notify()
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

