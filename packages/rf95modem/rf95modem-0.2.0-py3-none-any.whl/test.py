import serial
import serial.threaded
import sys
import time
import threading

import rf95modem


if __name__ == "__main__":
    ser = serial.serial_for_url("/dev/ttyUSB0", baudrate=115200, timeout=1)
    with serial.threaded.ReaderThread(ser, rf95modem.Rf95Reader) as rf95:
        rf95.rx_handlers.append(lambda rx: print(rx))

        rf95.mode(rf95modem.ModemMode.MEDIUM_RANGE)
        rf95.frequency(868.1)

        print(rf95.status_fetch())

        try:
            rf95.gps_mode(True)
            print(rf95.gps_fetch())
        except rf95modem.Rf95UnknownCommandException:
            print("Seems like there is no GPS support")

        rf95.transmit(b"hello world")

        threading.Event().wait()
