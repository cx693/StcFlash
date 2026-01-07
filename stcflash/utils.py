import argparse
import serial

class Utils:
    """Common utility functions"""

    @classmethod
    def to_bool(cls, val):
        """make sensible boolean from string or other type value"""

        if not val:
            return False
        if isinstance(val, bool):
            return val
        elif isinstance(val, int):
            return bool(val)
        return True if val[0].lower() == "t" or val[0] == "1" else False

    @classmethod
    def to_int(cls, val):
        """make int from any value, nice error message if not possible"""

        try:
            return int(val, 0)
        except (TypeError, ValueError):
            raise ValueError("invalid integer")

    @classmethod
    def hexstr(cls, bytestr, sep=""):
        """make formatted hex string output from byte sequence"""

        return sep.join(["%02X" % x for x in bytes(bytestr)])

    @classmethod
    def decode_packed_bcd(cls, byt):
        """Decode two-digit packed BCD value"""
        return (byt & 0x0f) + (10 * (byt >> 4))


class BaudType:
    """Check baud rate for validity"""

    def __call__(self, string):
        baud = int(string)
        if baud not in serial.Serial.BAUDRATES:
            raise argparse.ArgumentTypeError("illegal baudrate")
        return baud

    def __repr__(self):
        return "baudrate"
