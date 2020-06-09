#!/bin/sh

$ echo $PWD

sudo python3 $PWD/Desktop/wifiSniffingDistanceTest/netInterfaceSetting.py wlan1

sleep 3

sudo ./Desktop/wifiSniffingDistanceTest/New_sniffer/simplesniffer wlan1 eth0 0 0 127.0.0.1 