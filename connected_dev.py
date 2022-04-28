from scapy.all import *
from scapy.layers.dot11 import Dot11

devices = set()


def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        dot11_layer = pkt.getlayer(Dot11)

        if (dot11_layer.addr1 and (str(dot11_layer.addr1)).__eq__("7e:24:59:9b:e3:20") ) and (dot11_layer.addr2 and (dot11_layer.addr2 not in devices)):
            devices.add(dot11_layer.addr2)
            print(dot11_layer.addr2)


if __name__ == "__main__":
    # start the channel changer
    # channel_changer = Thread(target=change_channel)
    # channel_changer.daemon = True
    # channel_changer.start()
    sniff(iface="wlan1", count=10000, prn=PacketHandler)
