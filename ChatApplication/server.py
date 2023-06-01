#!/usr/bin/env python3
"""Asenkron multithreaded chat uygulaması için server."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Gelen client'lar için."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s bağlandı." % client_address)
        client.send(bytes("Kullanıcı adınızı giriniz", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # İstemci soketini argüman olarak alır.
    """Tek client için oturum sağlar."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Hoşgeldiniz %s! Çıkmak isterseniz, {quit} yazınız' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s Chate hoşgeldin!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s chatten ayrıldı" % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix isim tanımlaması içindir.
    """Bütün client lara broadcast."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Bağlantilar için bekliyor...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()