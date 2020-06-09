from sense_hat import SenseHat
import udpRecvForCSniffer as func
import concurrent.futures
import logging
import queue
import threading
import time
import math
import socket


def pressure2Altitude(Ph):
    p0 = 1013.25
    return (math.log(Ph / p0)) / -0.00012


def senseProducer(queue, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        pressure = sense.get_pressure()

        # sense.show_message(z)
        # print("x={0}, y={1}, z={2}".format(x, y, z))
        radioInfo_raw = {
            "type": "sense",
            "pressure": pressure
        }

        queue.put(radioInfo_raw)
        time.sleep(0.01)

    logging.info("Producer received event. Exiting")


def consumer(queue, event):
    """Pretend we're saving a number in the database."""
    altitude = 0
    while not event.is_set() or not queue.empty():
        message = queue.get()

        if message["type"] == "sense":
            altitude = pressure2Altitude(message["pressure"])
            print(altitude)
        else:

            # Syler, you can get the data in here
            # print(message, altitude)
            logging.info(
                "Consumer storing message: (size=%d) %s %s", queue.qsize(), message, altitude
            )


def snifferProducer(queue, event):
    while not event.is_set():
        data, addr = sock.recvfrom(1024)
        radioInfo_raw = {
            "type": "sniffer",
            'macAddress': func.getMacAddress(data),
            'RSSI': func.readInt8(data[20:21]),
            'ChannelFreq': func.readUInt16LE(data, 22),
            'snifferDeviceMac': func.formatMac(data.hex()[4:16]),
            'frameControl': func.BitArray(data[24:25]).bin
        }
        queue.put(radioInfo_raw)


if __name__ == '__main__':
    sense = SenseHat()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 7774)
    sock.bind(server_address)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    pipeline = queue.Queue(maxsize=1000)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(senseProducer, pipeline, event)
        executor.submit(snifferProducer, pipeline, event)
        executor.submit(consumer, pipeline, event)


        time.sleep(0.1)
        logging.info("Main: about to set event")
        # event.set()
