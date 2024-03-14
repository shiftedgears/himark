from Client import Client

class Room: # TODO: Ensure that this class uses Client objects rather than just strings
    def __init__(self, name: str = "default"):
        self.name = name
        self.clients = list()

    def get_client_list(self):
        return self.clients

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
