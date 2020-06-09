import struct
from datetime import datetime
import socket
import json
from bitstring import BitArray


def readUInt16LE(bytes, offset):
    return ((bytes[offset] & 0xff) | (bytes[offset + 1] << 8)) << 16 >> 16


def formatMac(raw_mac):
    raw_mac = ":".join(["%s" % (raw_mac[i:i + 2]) for i in range(0, 12, 2)])
    return raw_mac.upper()


def getMacAddress(rawData):
    mac_address_temp = ''

    for x in range(16, 28):
        mac_address_temp += rawData.hex()[x]
    mac_address_temp = ":".join(["%s" % (mac_address_temp[i:i + 2]) for i in range(0, 12, 2)])

    return mac_address_temp.upper()


def getRssiValue(rawData):
    return rawData[20] - 256


def readInt8(bytes):
    if len(bytes) != 1:
        print("Wrong number of bytes (" + str(len(bytes)) + ") should be 1")
        return None
    data, = struct.unpack("<b", bytes)
    return data


def received():
    i = 0
    time_period = 0
    start_time = datetime.now().timestamp() * 1000
    while time_period < 10000:
        data, addr = sock.recvfrom(1024)
        mac_address = getMacAddress(data)

        radioInfo_raw = {
            'timestamp': datetime.now().timestamp() * 1000,
            'macAddress': mac_address,
            'RSSI': readInt8(data[20:21]),
            'ChannelFreq': readUInt16LE(data, 22),
            'snifferDeviceMac': formatMac(data.hex()[4:16]),
            'frameControl': BitArray(data[24:25]).bin
        }

        # socket_zmq.send_string(json.dumps(radioInfo_raw))
        time_period = datetime.now().timestamp() * 1000 - start_time
        i = i + 1
        print('i= ', i)
        print("MAC Address:", mac_address, getRssiValue(data), readUInt16LE(data, 22), readUInt16LE(data, 24),
              data.hex(), len(data.hex()))
        print("FrameControl:", BitArray(data[24:25]).bin, "router_Mac:", formatMac(data.hex()[4:16]), "source_Mac:",
              formatMac(data.hex()[16:28]))
        print("\n")


if __name__ == "__main__":
    # context = zmq.Context()
    # socket_zmq = context.socket(zmq.PUB)
    # socket_zmq.bind("tcp://*:5555")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 7774)

    sock.bind(server_address)

    received()
