from scapy.all import *
from scapy.layers.dot11 import Dot11Deauth, Dot11
from getmac import get_mac_address as gma
from subprocess import *

count = 0


def my_mac():
    return gma(interface="wlx5ca6e6a2e6c8")


def sniff_de_auth(pkt):
    my_mac_addr = my_mac()
    global count
    if pkt.haslayer(Dot11Deauth):
        dot11_layer = pkt.getlayer(Dot11)
        if (dot11_layer.addr1 and (str(dot11_layer.addr1)).__eq__(my_mac_addr)) or \
                (dot11_layer.addr2 and (str(dot11_layer.addr2)).__eq__(my_mac_addr)):
            count += 1
    if count >= 10:
        print("WARNING! DeAuth attack detected\nEvilTwin attack suspicion!")
        call(["sudo", "ifconfig", "wlx5ca6e6a2e6c8", "down"])


sniff(iface="wlan0", prn=sniff_de_auth)
