import board
import usb_hid
from adafruit_hid.mouse import Mouse
import adafruit_nunchuk

m = Mouse(usb_hid.devices)
nc = adafruit_nunchuk.Nunchuk(board.I2C())

centerX = 128
centerY = 128

scaleX = 0.3
scaleY = 0.3

cDown = False
zDown = False

while True:
    # get current nunchuk values
    values = nc.values

    # the ones we use here
    x = values.jx
    y = values.jy
    c = values.C
    z = values.Z

    # skip spurious reads
    if x == 255 or y == 255:
        continue

    # add offsets
    relX = x - centerX
    relY = centerY - y

    # move cursor
    m.move(int(scaleX * relX), int(scaleY * relY), 0)

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
