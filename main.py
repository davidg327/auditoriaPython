from tkinter import *
import threading
import os
import re
from tkinter import ttk
import subprocess

def get_mac(text):
    return re.findall(r'([\w]{2}(?::[\w]{2}){5})', text)

def get_ip(text):
    return re.findall('[0-1][0-9][0-9]\.[0-9][0-9][0-9]\.[0-9][0-9]\.\d*\s', text)

def devices():
    text = os.popen('sudo nast -m -i eth0').read()
    mac = get_mac(text)
    ip = get_ip(text)
    i = 0
    len_mac = len(mac)
    while i < len_mac:
        tv.insert("", END, text=i, values=(ip[i], mac[i]))
        i += 1
    else:
        print ('no se encontraron más dispositivos')

def PrincipalThread():
    threading.Thread(target=devices).start()


window = Tk()
window.title('Proyecto final')


tv = ttk.Treeview(window, columns=("col1", "col2"))
tv.pack()

tv.column("#0", width=160)
tv.column("col1", width=160, anchor=CENTER)
tv.column("col2", width=400, anchor=CENTER)

tv.heading("#0", text="Id", anchor=CENTER)
tv.heading("col1", text="IP", anchor=CENTER)
tv.heading("col2", text="MAC", anchor=CENTER)


Button(window, text='Ver Dispositivos', command=PrincipalThread).pack()


window.mainloop()





