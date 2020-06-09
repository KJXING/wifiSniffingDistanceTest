import os
import sys


def wirelessInterfaceCongfig(iface):
    os.system('sudo ifconfig %s down' % iface)
    os.system('sudo iwconfig %s mode monitor' % iface)
    os.system('sudo ifconfig %s up' % iface)
    print("Successfully Process!")


if __name__ == '__main__':

    if (len(sys.argv) == 2):
        wirelessInterfaceCongfig(sys.argv[1])
    else:
        print("Please input the wireless Interface. \n Example: sudo python3 netInterfaceSetting wlan1")
