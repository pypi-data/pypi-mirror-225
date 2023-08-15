# rf95modem-py

Python library to send and receive data over LoRa PHY via a serial connection to a [rf95modem].

This library was tested against the rf95modem commit [`8f163aa`][rf95modem-commit], slightly after version 0.7.3.


## Install

This library is available on PyPI as [`rf95modem`][pypi-rf95modem].

```
pip install --upgrade rf95modem
```

## Library

The primary focus of this library is to send and receive data via LoRa's physical layer, LoRa PHY, with the help of a [rf95modem].

Therefore the `rf95modem.reader.Rf95Reader.` allows direct interaction with a connected rf95modem, including configuration changes, sending, and receiving raw LoRa PHY messages.
This `Rf95Reader` extends `serial.threaded.LineReader` from [pySerial][pyserial].

The following short code example demonstrates how to use this library.

```python
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
```


## Documentation

```
pip install --upgrade pdoc3

cd src
pdoc --http 127.0.0.1:8080 rf95modem
xdg-open http://127.0.0.1:8080/
```


## Build a Release
- Bump the `project.version` in the `pyproject.toml` file.
- `python3 -m build`


[pypi-rf95modem]: https://pypi.org/project/rf95modem/
[pyserial]: https://github.com/pyserial/pyserial/
[rf95modem-commit]: https://github.com/gh0st42/rf95modem/commit/8f163aa23e6f0c1ca7403c13b0811366e40b7317
[rf95modem]: https://github.com/gh0st42/rf95modem
