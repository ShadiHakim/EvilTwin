#!/use/bin/env python3

from subprocess import call
from time import sleep

#call(["sudo", "service", "apache2", "start"])
#call(["sudo", "service", "dnsmasq", "start"])
#call(["sudo", "php", "-S", "127.0.0.1:80", "-t", "html/" ,"&"])
sleep(1)


call(["sudo", "ifconfig", "wlo1", "up", "10.0.10.1", "netmask", "255.255.255.0"])
sleep(1)
call(["sudo", "route", "add", "-net", "10.0.10.0", "netmask", "255.255.255.0", "gw", "10.0.10.1"])
sleep(1)

# call(["sudo", "udhcpd"])
sleep(1)

call(["sudo", "dnsmasq", "-C", "dnsmasq.conf"])
call(["sudo", "hostapd", "hostapd.conf"])
