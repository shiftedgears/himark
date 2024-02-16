import requests
from requests.exceptions import ConnectionError

ip = "127.0.0.1"
port = "8000"

try:
    url = f"http://{ip}:{port}"
    response = requests.get(f"{url}/BBS")

    print(response)

    print(response.json())

    cmd = input("CMD>:")

    data = {"arg1":cmd}

    response = requests.post(f"{url}/connecting", json=data)

    print(response.json())

except ConnectionError:
    print(f"ERR: No himark server")
