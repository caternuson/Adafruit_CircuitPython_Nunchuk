import time
import board
import busio
import adafruit_nunchuk

i2c = busio.I2C(board.SCL, board.SDA, frequency=375000)

nc = adafruit_nunchuk.Nunchuk(i2c)

while True:
    x, y = nc.joystick
    ax, ay, az = nc.acceleration
    print("joystick = {},{}".format(x, y))
    print("accceleration ax={}, ay={}, az={}".format(ax, ay, az))
    if nc.button_C:
        print("button C")
    if nc.button_Z:
        print("button Z")
    time.sleep(0.5)
