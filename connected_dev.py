import signal
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon

devices = set()
ap = ""


def packet_handler(pkt):
    if pkt.haslayer(Dot11) and not pkt.haslayer(Dot11Beacon):
        dot11_layer = pkt.getlayer(Dot11)

        if (dot11_layer.addr1 and (str(dot11_layer.addr1)).__eq__(ap)) and (
                dot11_layer.addr2 and (dot11_layer.addr2 not in devices)):
            devices.add(dot11_layer.addr2)
            print(dot11_layer.addr2)


if __name__ == "__main__":
    ap = sys.argv[1:2].pop()
    print("Connected devices: ")
    sniff(iface="wlx00c140610e6c", count=10000, prn=packet_handler, timeout=60)
