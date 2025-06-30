import time
import board

import adafruit_seesaw.seesaw

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

from collections import deque
import math

from collections import deque
import math

class RobustNormalizer:
    def __init__(
        self,
        decay=0.01,
        outlier_stddev=2.0,
        avg_window=5,
        buffer_size=50,
        fixed_min=None,
        fixed_max=None
    ):
        self.decay = decay
        self.outlier_stddev = outlier_stddev
        self.avg_window = avg_window
        self.buffer_size = buffer_size
        self.fixed_min = fixed_min
        self.fixed_max = fixed_max

        self.buffer = deque(maxlen=buffer_size)
        self.smooth_buffer = deque(maxlen=avg_window)

        self.min_val = None
        self.max_val = None
        self.last_output = 0.0

    def mean_std(self):
        n = len(self.buffer)
        if n == 0:
            return 0, 0
        mean = sum(self.buffer) / n
        variance = sum((x - mean) ** 2 for x in self.buffer) / n
        stddev = math.sqrt(variance)
        return mean, stddev

    # def is_outlier(self, x):
    #     if len(self.buffer) < 5:
    #         return False
    #     mean, stddev = self.mean_std()
    #     return abs(x - mean) > self.outlier_stddev * stddev

    def normalize(self, x):
        # if self.is_outlier(x):
        #     print(f"Filtered outlier: {x}")
        #     return self.last_output

        self.buffer.append(x)

        # Determine normalization bounds
        min_val = self.fixed_min
        max_val = self.fixed_max

        if min_val is None or max_val is None:
            # Adaptive min/max
            if self.min_val is None or self.max_val is None:
                self.min_val = self.max_val = x
            else:
                if x < self.min_val:
                    self.min_val = x
                else:
                    self.min_val += self.decay * (x - self.min_val)

                if x > self.max_val:
                    self.max_val = x
                else:
                    self.max_val += self.decay * (x - self.max_val)

            min_val = self.min_val
            max_val = self.max_val

        # Normalize
        if max_val == min_val:
            norm = 0.0
        else:
            norm = (x - min_val) / (max_val - min_val)
            norm = max(0.0, min(1.0, norm))  # Clamp to [0, 1]

        # Smooth with moving average
        self.smooth_buffer.append(norm)
        smoothed = sum(self.smooth_buffer) / len(self.smooth_buffer)

        self.last_output = smoothed
        return smoothed

send_adc = True
print_osc = False
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

normalizer0 = RobustNormalizer(fixed_min=19000, fixed_max=26000)
normalizer1 = RobustNormalizer(fixed_min=18000, fixed_max=26000)

print("Starting adc loop \n")
# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    #read adc
    current_time = time.time()
    if current_time - last_time > 0.1: #sampling interval
        last_time = current_time
        # Build a message with autodetection of data types, and send it.
        if send_adc:
            msg = oscbuildparse.OSCMessage("/adc", None, [normalizer0.normalize(adcChan0.value), normalizer1.normalize(adcChan1.value)])
            osc_send(msg, "client")
            if print_osc:
                print(msg)
    
    # You can send OSC messages from your event loop too…
    osc_process()
    
# Properly close the system.
osc_terminate()