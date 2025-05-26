# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0-3
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)


# print("{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}".format("raw0", "v0", "raw1", "v1", "raw2", "v2", "raw3", "v3",))

# while True:
#     print("{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}\t{:>5}".format(chan0.value, chan0.voltage, chan1.value, chan1.voltage, chan2.value, chan2.voltage, chan3.value, chan3.voltage))
#     time.sleep(0.4)

print("{:>5}\t{:>5}\t{:>5}\t{:>5}".format("raw0", "raw1", "raw2", "raw3"))

while True:
    # print encoder values
    print("{:>5}\t{:>5}\t{:>5}\t{:>5}".format(chan0.value, chan1.value, chan2.value, chan3.value))
    time.sleep(0.05)