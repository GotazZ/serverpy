import socket

HOST = '192.168.1.28'
PORT = 8000

# Demande à l'utilisateur de choisir le premier message
first_message = input("Choisissez le premier message ('nouveau' ou 'delete') : ").strip().lower()
while first_message not in ['nouveau', 'delete']:
    print("Choix invalide. Entrez 'nouveau' ou 'delete'.")
    first_message = input("Choisissez le premier message ('nouveau' ou 'delete') : ").strip().lower()

# Demande à l'utilisateur d'entrer le deuxième message
second_message = input("Entrez le deuxième message (ex: nom du MenuEntry) : ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"En écoute sur {HOST}:{PORT}...")

    conn, addr = s.accept()
    with conn:
        print('Connecté par', addr)

        # Envoie le premier message
        conn.sendall(first_message.encode('utf-8'))

        # Envoie le deuxième message
        conn.sendall(second_message.encode('utf-8'))
