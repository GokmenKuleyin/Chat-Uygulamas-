#!/usr/bin/env python3
"""Tkinter GUI'ı için."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Mesajları almak için."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Muhtemelen client sohbetten ayrıldı.
            break


def send(event=None):
    """Mesajları göndermek için."""
    msg = my_msg.get()
    my_msg.set("")  # Inputu temizler.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """Eğer pencere kapatilirsa."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Whatsapp")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Gönderilen mesajlar için
my_msg.set("Mesajınızı buraya yazınız.")
scrollbar = tkinter.Scrollbar(messages_frame)  # Geçmiş mesajlar arasında gezinmek için.
# Alttaki kodlar mesajları içerir.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Gönder", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Soket kısmıı aşağıda----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # GUI'ı execute eder.