import time
import board

import adafruit_seesaw.seesaw

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

send_adc = True
print_osc = True
ip = "127.0.0.1"
port = 57120

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client(ip, port, "client")

# use default I2C bus
i2c = board.I2C()

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)

last_time = 0

# Create single-ended input on channel 0-3
adcChan0 = AnalogIn(ads, ADS.P0)
adcChan1 = AnalogIn(ads, ADS.P1)
adcChan2 = AnalogIn(ads, ADS.P2)
adcChan3 = AnalogIn(ads, ADS.P3)

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    #read adc
    current_time = time.time()
    if current_time - last_time > 0.01: #sampling interval
        last_time = current_time;
        # Build a message with autodetection of data types, and send it.
        if send_adc:
            msg = oscbuildparse.OSCMessage("/adc", None, [adcChan0.value, adcChan1.value, adcChan2.value, adcChan3.value])
            osc_send(msg, "client")
            if print_osc:
                print(msg)
    
    # You can send OSC messages from your event loop too…
    osc_process()
    
# Properly close the system.
osc_terminate()