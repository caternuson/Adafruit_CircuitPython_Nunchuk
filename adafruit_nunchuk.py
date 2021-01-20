# The MIT License (MIT)
#
# Copyright (c) 2019 Carter Nelson for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_nunchuk`
================================================================================

CircuitPython library for Nintendo Nunchuk controller


* Author(s): Carter Nelson

Implementation Notes
--------------------

**Hardware:**

* `Wii Remote Nunchuk <https://en.wikipedia.org/wiki/Wii_Remote#Nunchuk>`_
* `Wiichuck <https://www.adafruit.com/product/342>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""
import time
from collections import namedtuple
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Nunchuk.git"

_DEFAULT_ADDRESS = 0x52
_I2C_INIT_DELAY = 0.1
_I2C_READ_DELAY = 0.01


class Nunchuk:
    """Class which provides interface to Nintendo Nunchuk controller."""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.buffer = bytearray(6)
        self.i2c_device = I2CDevice(i2c, address)
        time.sleep(_I2C_INIT_DELAY)
        with self.i2c_device as i2c_dev:
            # turn off encrypted data
            # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
            i2c_dev.write(b"\xF0\x55")
            time.sleep(_I2C_INIT_DELAY)
            i2c_dev.write(b"\xFB\x00")

    @property
    def values(self):
        """All values as a named tuple."""
        self._read_data()
        return namedtuple("Values", ("jx", "jy", "C", "Z", "ax", "ay", "az"))(
            self.buffer[0],
            self.buffer[1],
            not bool(self.buffer[5] & 0x02),
            not bool(self.buffer[5] & 0x01),
            ((self.buffer[5] & 0xC0) >> 6) | (self.buffer[2] << 2),
            ((self.buffer[5] & 0x30) >> 4) | (self.buffer[3] << 2),
            ((self.buffer[5] & 0x0C) >> 2) | (self.buffer[4] << 2)
        )

    @property
    def joystick(self):
        """The joystick position."""
        v = self.values
        return v.jx, v.jy

    @property
    def button_C(self):  # pylint: disable=invalid-name
        """The pressed state of button C."""
        return self.values.C

    @property
    def button_Z(self):  # pylint: disable=invalid-name
        """The pressed state of button Z."""
        return self.values.Z

    @property
    def acceleration(self):
        """The acceleration as a 3 tuple."""
        v = self.values
        return v.ax, v.ay, v.az

    def _read_data(self):
        # read all of the current data into local buffer via a single (slow) i2c xfer
        with self.i2c_device as i2c:
            time.sleep(_I2C_READ_DELAY)
            i2c.write(b"\x00")
            time.sleep(_I2C_READ_DELAY)
            i2c.readinto(self.buffer)
