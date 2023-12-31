import socket
import cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

import threading


parse = []
def process_command(cmd):
    """
    Fonction pour traiter les commandes
    """
    parse = cmd.split()

    if parse:
        if parse[0] == "new":
            try:
                print(parse[1])
                open_port(int(parse[1]))
                receiver_t = threading.Thread(target=receiver, args=(int(parse[1]),))
                receiver_t.start()
            except Exception as e:
                print(f"Erreur dans l'ajout du nouveau client : {e}")
        elif parse[0] == "kill":
            if parse[1] == "all":
                kill_all()
            elif not parse[1]:
                print("il manque un argument")
            else:
                print(close_port(int(parse[1])))
                print("Client(s) sur port " + parse[1] + " terminated")

    # Réinitialiser la liste parse
    parse = []

    return bool(parse)


def commands():
    """
    La fonction demande un
    La fonction ne retourne rien
    """

    while True:
        cmd = input(">>> ")

        if not process_command(cmd):
            break

        if touchenter():
            break


# Appel de la fonction principale
commands()
def dechiffrement(data):
    private_key_path = 'srv/siproject_private.pem'
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    dec_data = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return dec_data.decode('utf-8')


def chiffrement(data):
    pub_public_key = "client/siproject.pem"

    with open(pub_public_key, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    d_enc = data.encode('utf-8')
    enc_data = public_key.encrypt(
        d_enc,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return enc_data


def envoi():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5000))

    data = "ffffffffffffffffffff"

    client_socket.send(chiffrement(data))  # envoi
    client_socket.close()


def ecoute():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(1)

    print("Ecoute")

    client_socket, client_address = server_socket.accept()
    print(f"connexion de {client_address}")

    # recu data
    data = client_socket.recv(1024)
    print(dechiffrement(data))

    print("connexion")
    client_socket.close()
    server_socket.close()


# Vous pouvez éviter de donner les mêmes noms aux fonctions et aux threads
thread_ecoute = threading.Thread(target=ecoute)
thread_envoi = threading.Thread(target=envoi)

thread_ecoute.start()
thread_envoi.start()

# Assurez-vous que les threads ont terminé avant de terminer le programme
thread_ecoute.join()
thread_envoi.join()

# data.encode('utf-8')
# data = chiffrement(data)
# print(data)
# print(dechiffrement(data))
