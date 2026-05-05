# src/serial_comm.py
import time
import serial
import serial.tools.list_ports

# Candidate ports tried in order on each platform
_LINUX_PORTS = ["/dev/ttyUSB0", "/dev/ttyACM0"]
_WINDOWS_PORTS = [f"COM{i}" for i in range(3, 10)]


def _find_port() -> str:
    """Return first available serial port, or raise RuntimeError."""
    import sys
    candidates = _WINDOWS_PORTS if sys.platform == "win32" else _LINUX_PORTS
    for port in candidates:
        try:
            s = serial.Serial(port)
            s.close()
            return port
        except (serial.SerialException, OSError):
            continue
    raise RuntimeError(
        f"No Arduino found. Tried: {candidates}\n"
        "Connect the Arduino and check the port, or pass port= explicitly."
    )


class SerialComm:
    def __init__(self, port: str = None, baud: int = 9600):
        self._port = port
        self._baud = baud
        self._ser: serial.Serial = None

    def connect(self):
        port = self._port or _find_port()
        self._ser = serial.Serial(port, self._baud, timeout=1)
        time.sleep(2)  # wait for Arduino reset after DTR toggle
        print(f"[Serial] Connected on {port} @ {self._baud} baud")

    def send(self, command: str):
        if self._ser and self._ser.is_open:
            self._ser.write((command + "\n").encode())

    def close(self):
        if self._ser and self._ser.is_open:
            self._ser.close()
