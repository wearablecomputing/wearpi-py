import time
import board
import digitalio

import adafruit_seesaw.digitalio
import adafruit_seesaw.rotaryio
import adafruit_seesaw.seesaw

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_neokey.neokey1x4 import NeoKey1x4

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("192.168.1.29", 57120, "client")

# use default I2C bus
i2c = board.I2C()

# Create a NeoKey object
neokey = NeoKey1x4(i2c, addr=0x30)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)

encoders = [adafruit_seesaw.rotaryio.IncrementalEncoder(seesaw, n) for n in range(4)]
switches = [adafruit_seesaw.digitalio.DigitalIO(seesaw, pin) for pin in (12, 14, 17, 9)]
for switch in switches:
    switch.switch_to_input(digitalio.Pull.UP)  # input & pullup!

last_positions = [0, 0, 0, 0]
enc_rot = [0, 0, 0, 0]
last_enc_button = [True, True, True, True]

button_vals = [False, False, False, False]
last_button = [False, False, False, False]

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
    if current_time - last_time > 0.05:
        last_time = current_time;
        # print("/adc, {:>5}, {:>5}, {:>5}, {:>5}".format(adcChan0.value, adcChan1.value, adcChan2.value, adcChan3.value))
        # Build a message with autodetection of data types, and send it.
        # msg = oscbuildparse.OSCMessage("/adc", None, [adcChan0.value, adcChan1.value, adcChan2.value, adcChan3.value])
        # osc_send(msg, "sc_client")
    
    # read encoders
    changed = False
    positions = [encoder.position for encoder in encoders]
    for n, rotary_pos in enumerate(positions):
        if rotary_pos != last_positions[n]:
            changed = True
            if rotary_pos > last_positions[n]: 
                enc_rot[n] = 1;
                # print(f"Rotary #{n}: UP")
            else:
                if rotary_pos < last_positions[n]:
                    enc_rot[n] = -1;
                    # print(f"Rotary #{n}: DOWN")
            last_positions[n] = rotary_pos
        else:
            enc_rot[n] = 0;
            
    if changed:
        msg = oscbuildparse.OSCMessage("/enc-rot", None, enc_rot)
        osc_send(msg, "client")

    changed = False
    switch_vals = [switch.value for switch in switches]
    for n, enc_button in enumerate(switch_vals):
        if enc_button != last_enc_button[n]:
            last_enc_button[n] = enc_button
            changed = True
            # if not enc_button:
                # print(f"Encoder Button #{n}: pressed")
            # else:
                # print(f"Encoder Button #{n}: released")
            
    if changed:
        enc_but = [int(not button) for button in switch_vals]
        msg = oscbuildparse.OSCMessage("/enc-but", None, enc_but)
        osc_send(msg, "client")
#read buttons
    changed = False
    for n, button_val, in enumerate(button_vals):
        button_val = neokey[n]
        if button_val != last_button[n]:
            changed = True
            # if button_val:
                # print(f"Button #{n}: pressed")
            # else:
                # print(f"Button #{n}: released")
        last_button[n] = neokey[n]
    if changed:
        keys = [int(key) for key in [neokey[3],neokey[2], neokey[1], neokey[0]] ]
        msg = oscbuildparse.OSCMessage("/key", None, keys)
        osc_send(msg, "client")


    # You can send OSC messages from your event loop too…
    osc_process()
    

# Properly close the system.
osc_terminate()