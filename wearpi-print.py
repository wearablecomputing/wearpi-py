import time
import board
import digitalio

import adafruit_seesaw.digitalio
import adafruit_seesaw.rotaryio
import adafruit_seesaw.seesaw

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_neokey.neokey1x4 import NeoKey1x4

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
last_enc_button = [True, True, True, True]

button_vals = [False, False, False, False]
last_button = [False, False, False, False]


# Create single-ended input on channel 0-3
adcChan0 = AnalogIn(ads, ADS.P0)
adcChan1 = AnalogIn(ads, ADS.P1)
adcChan2 = AnalogIn(ads, ADS.P2)
adcChan3 = AnalogIn(ads, ADS.P3)

# print("{:>5}\t{:>5}\t{:>5}\t{:>5}".format("raw0", "raw1", "raw2", "raw3"))

while True:
    #read adc
    print("/wearpi/adc, {:>5}, {:>5}, {:>5}, {:>5}".format(adcChan0.value, adcChan1.value, adcChan2.value, adcChan3.value))
    
    # read encoders
    positions = [encoder.position for encoder in encoders]
    for n, rotary_pos in enumerate(positions):
        if rotary_pos != last_positions[n]:
            if rotary_pos > last_positions[n]:  
                print(f"Rotary #{n}: UP")
            else:
                print(f"Rotary #{n}: DOWN")
            last_positions[n] = rotary_pos

        switch_vals = [switch.value for switch in switches]
        if switch_vals[n] != last_enc_button[n]:
            if not switch_vals[n]:
                print(f"Encoder Button #{n}: pressed")
            else:
                print(f"Encoder Button #{n}: released")
            last_enc_button[n] = switch_vals[n]

#read buttons
    for n, button_val, in enumerate(button_vals):
        button_val = neokey[n]
        if button_val != last_button[n]:
            if button_val:
                print(f"Button #{n}: pressed")
            else:
                print(f"Button #{n}: released")
        last_button[n] = neokey[n]
    time.sleep(0.05)