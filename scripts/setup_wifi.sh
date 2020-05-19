#!/bin/bash

####################################################################
# Description: Script to configure wifi settings. Script is based on
# instructions provided at
# https://pimylifeup.com/raspberry-pi-wireless-access-point/
# Author: Kenny Robinson, @almostengr
# Created: 2017-05-15
####################################################################

DATETTIME=$(date +%Y%m%d%H%M)

function log_message() {
# print message to screen and to log file
	echo $*
	echo "$(date) | "$* >> /var/tmp/trafficpi${DATETIME}/raspitraffic_setup.log
}

# CHECK TO SEE IF THE SCRIPT IS BEING RAN AS ROOT
if [ $(id -u) -eq 0 ]; then
	# step 0 
	log_message "Making backup directory"
	mkdir /var/tmp/trafficpi${DATETIME}

	log_message "Uninstalling existing packages and configuration"
	apt-get autoremove --purge hostapd dnsmasq -y

	log_message "Performing wifi Setup"

	log_message "Backups of files will be saved in /var/tmp/trafficpi${DATETIME}"

	# step 1
	apt-get update
	apt-get upgrade -y
	
	# step 2
	log_message "Installing software"
	apt-get install hostapd dnsmasq -y
	
	# step 3
	log_message "Stoping services"
	systemctl stop hostapd
	systemctl stop dnsmasq

	# step 4 and 5
	log_message "Updating dhcpcd.conf"
	touch /etc/dhcpcd.conf

	# make backup of original file
	cp -p /etc/dhcpcd.conf /var/tmp/trafficpi${DATETIME}

	echo "interface wlan0" >> /etc/dhcpcd.conf
	echo "static ip_address=192.168.220.1/24" >> /etc/dhcpcd.conf
	echo "nohook wpa_supplicant" >> /etc/dhcpcd.conf

	# step 6
	log_message "Restarting DHCPCD"
	systemctl restart dhcpcd 

	# step 7 and 8
	log_message "Updating hostapd.conf"
	touch /etc/hostapd/hostapd.conf

	# make backup of original file
	cp -p /etc/hostapd/hostapd.conf /var/tmp/trafficpi${DATETIME}

	echo "interface=wlan0" >> /etc/hostapd/hostapd.conf
	echo "driver=nl80211" >> /etc/hostapd/hostapd.conf
	echo "hw_mode=g" >> /etc/hostapd/hostapd.conf
	echo "channel=6" >> /etc/hostapd/hostapd.conf
	echo "ieee80211n=1" >> /etc/hostapd/hostapd.conf
	echo "wmm_enabled=0" >> /etc/hostapd/hostapd.conf
	echo "macaddr_acl=0" >> /etc/hostapd/hostapd.conf
	echo "ignore_broadcast_ssid=0" >> /etc/hostapd/hostapd.conf
	echo "auth_algs=1" >> /etc/hostapd/hostapd.conf
	echo "wpa=2" >> /etc/hostapd/hostapd.conf
	echo "wpa_key_mgmt=WPA-PSK" >> /etc/hostapd/hostapd.conf
	echo "wpa_pairwise=TKIP" >> /etc/hostapd/hostapd.conf
	echo "rsn_pairwise=CCMP" >> /etc/hostapd/hostapd.conf
	echo "# This is the name of the network" >> /etc/hostapd/hostapd.conf
	echo "ssid=TrafficPi" >> /etc/hostapd/hostapd.conf
	echo "# The network passphrase" >> /etc/hostapd/hostapd.conf
	echo "wpa_passphrase=almostengr" >> /etc/hostapd/hostapd.conf

	# step 9 and 10
	log_message "Updating hostapd"
	cp -rp /etc/default /var/tmp/trafficpi${DATETIME}/
	/bin/sed 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|g' /var/tmp/trafficpi${DATETIME}/default/hostapd > /etc/default/hostapd

	# step 11 and 12
	cp -rp /etc/init.d /var/tmp/trafficpi${DATETIME}/init.d.hostapd
	/bin/sed 's|#DAEMON_CONF=|DAEMON_CONF=/etc/hostapd/hostapd.conf|g' /var/tmp/trafficpi${DATETIME}/init.d/hostapd > /etc/init.d/hostapd

	# step 13
	mv /etc/dnsmasq.conf /etc/dnsmasq.conf.${DATETIME}

	# step 14 and 15
	touch /etc/dnsmasq.conf
	echo "interface=wlan0       # Use interface wlan0" >> /etc/dnsmasq.conf
	echo "server=1.1.1.1       # Use Cloudflare DNS" >> /etc/dnsmasq.conf
	echo "dhcp-range=192.168.220.50,192.168.220.150,12h # IP range and lease time" >> /etc/dnsmasq.conf

	# step 16 and 17
	cp -p /etc/sysctl.conf /etc/sysctl.conf.${DATETIME}
	/bin/sed 's|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|g' /etc/sysctl.conf.${DATETIME} > /etc/sysctl.conf

	# step 18
	sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

	# step 19
	iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

	# step 20
	sh -c "iptables-save > /etc/iptables.ipv4.nat"
	
	# step 21 and 22
	cp -p /etc/rc.local /etc/rc.local.${DATETIME}
	/bin/sed 's|exit 0|iptables-restore < /etc/iptables.ipv4.nat|g' /etc/rc.local.${DATETIME} /etc/rc.local
	echo "" >> /etc/rc.local
	echo "exit 0" >> /etc/rc.local

	# step 23
	service hostapd start
	service dnsmasq start

	# step 24
	log_message "Raspberry Pi will reboot in 10 seconds"
	wait 10
	reboot

	log_message "Done performing Wifi setup"
	exit 0
else
	log_message "Must be root to run script."
	exit 1
fi
