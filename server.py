import socket
import threading
import time

clients = {}

def handle_client(conn, addr):
    client_id = conn.recv(1024).decode()  # attend un nom/id du client
    clients[client_id] = {"addr": addr, "last_seen": time.time(), "conn": conn}
    try:
    host_name = socket.gethostbyaddr(addr[0])[0]
    except socket.herror:
        host_name = addr[0]  # en cas d'échec, on garde l'IP

    print(f"{client_id} connecté depuis {host_name}")


    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            clients[client_id]["last_seen"] = time.time()
            print(f"Reçu de {client_id} : {data.decode()}")
    except:
        pass

    print(f"{client_id} déconnecté")
    clients[client_id]["connected"] = False
    conn.close()

def monitor_clients():
    while True:
        now = time.time()
        for client_id, info in list(clients.items()):
            if now - info["last_seen"] > 30:  # déconnecté si plus de 30 sec d'inactivité
                print(f"{client_id} est inactif")
        time.sleep(10)

# Lancer le serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('https://serverpy-jbkj.onrender.com', 5000))
server.listen(5)
print("Serveur en écoute sur le port 5000")

threading.Thread(target=monitor_clients, daemon=True).start()

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
