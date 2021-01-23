import board
import busio
import usb_hid
from adafruit_hid.mouse import Mouse
import adafruit_nunchuk

i2c = busio.I2C(board.SCL, board.SDA, frequency=375000)
nc = adafruit_nunchuk.Nunchuk(i2c)

m = Mouse(usb_hid.devices)

centerX = 128
centerY = 128

scaleX = 0.3
scaleY = 0.3

cDown = False
zDown = False

while True:
    x, y = nc.joystick

    # skip spurious reads
    if x == 255 or y == 255:
        continue

    # add offsets
    relX = x - centerX
    relY = centerY - y

    # move cursor
    m.move(int(scaleX * relX), int(scaleY * relY), 0)

    c = nc.button_C
    z = nc.button_Z

    # left click
    if z and not zDown:
        m.press(Mouse.LEFT_BUTTON)
        zDown = True
    elif not z and zDown:
        m.release(Mouse.LEFT_BUTTON)
        zDown = False

    # right click
    if c and not cDown:
        m.press(Mouse.RIGHT_BUTTON)
        cDown = True
    elif not c and cDown:
        m.release(Mouse.RIGHT_BUTTON)
        cDown = False
