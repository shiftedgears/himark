import requests
from requests.exceptions import ConnectionError

ip = "127.0.0.1"
port = "8000"

CLIENT_INIT_CONNECTION_MESSAGE = "HIMARK"
SERVER_INIT_CONNECTION_RESPONSE = "HEYJOHNNY"


try:
    url = f"http://{ip}:{port}"
    response = requests.get(f"{url}/BBS")

    print(response)

    print(response.json())

    data = {"arg1":CLIENT_INIT_CONNECTION_MESSAGE}

    response = requests.post(f"{url}/connection_attempt", json=data)
    
    if(response.json() != {'arg2':SERVER_INIT_CONNECTION_RESPONSE}): #if the server is not running
        sys.exit("ERR: Not a himark server")
    
    #otherwise there is a server running, enter into while loop for client
    

    print(response.json())

except ConnectionError:
    print(f"ERR: No himark server")
