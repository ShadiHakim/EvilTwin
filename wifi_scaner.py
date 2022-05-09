from scapy.all import *
from threading import Thread
import pandas
import time
import os

# initialize the networks dataframe that will contain all access points nearby
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt

interface = "wlx00c140610e6c"
flag = True
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)


def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        networks.loc[bssid] = (ssid, dbm_signal, channel)


def print_all():
    while flag:
        os.system("clear")
        if networks.empty:
            print("Please wait...")
        else:
            print(networks)
        time.sleep(0.5)


def change_channel():
    ch = 1
    while flag:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(0.5)


def get_networks():
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    printer.join(timeout=60)
    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    channel_changer.join(timeout=60)
    # start sniffing
    sniff(prn=callback, iface=interface, timeout=60)

    global flag
    flag = False

    return networks
