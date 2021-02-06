import socket, json
import requests

config = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()

HOST =  config["socket"]["host"]
PORT =  config["socket"]["puerto"]

def enviar(msg: str="Usuario no puso nada lel XD"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
        except:
            print("No tienes el socket activado!!!")
        cliente.sendall(f"{msg}".encode())

        data = cliente.recv(1024).decode()
        msg = json.loads(data)
        cliente.close()
        return msg["mensage"]