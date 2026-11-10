import time
import board

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

def log(message):
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}")


class I2CErrorReporter:
    """Rate-limited reporting of I2C read errors.

    A single failed I2C read (e.g. OSError [Errno 121] Remote I/O error from a
    loose cable or noise on the bus) should not kill the script: the caller
    skips that sample and retries. This class logs the first failure, then a
    reminder every `report_every` seconds while failures continue, and a
    summary once reads succeed again, so a flaky bus can't flood the log.
    """

    def __init__(self, name, report_every=5.0):
        self.name = name
        self.report_every = report_every
        self.failing_since = None  # time of first failure in the current run of failures
        self.count = 0             # failed reads in the current run
        self.total = 0             # failed reads since start
        self.last_report = 0

    def error(self, e):
        now = time.time()
        self.count += 1
        self.total += 1
        if self.failing_since is None:
            self.failing_since = now
            self.last_report = now
            log(f"{self.name}: I2C read failed ({e}), skipping sample and retrying")
        elif now - self.last_report >= self.report_every:
            self.last_report = now
            log(f"{self.name}: I2C still failing after {now - self.failing_since:.0f}s "
                f"({self.count} failed reads), last error: {e}")

    def ok(self):
        if self.failing_since is not None:
            log(f"{self.name}: I2C recovered after {self.count} failed read(s) over "
                f"{time.time() - self.failing_since:.1f}s ({self.total} failed reads since start)")
            self.failing_since = None
            self.count = 0


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



last_time = 0

# Create single-ended input on channel 0-3
adcChan0 = AnalogIn(ads, 0)
adcChan1 = AnalogIn(ads, 1)
adcChan2 = AnalogIn(ads, 2)
adcChan3 = AnalogIn(ads, 3)

normalizer0 = RobustNormalizer(fixed_min=1000, fixed_max=12000)
normalizer1 = RobustNormalizer(fixed_min=1000, fixed_max=12000)
normalizer2 = RobustNormalizer(fixed_min=8000, fixed_max=13000)
normalizer3 = RobustNormalizer(fixed_min=900, fixed_max=1200)

adc_errors = I2CErrorReporter("ADC (ADS1115)")

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
            # Read all four channels first, so a failed read doesn't leave
            # some normalizers updated and others not.
            try:
                raw = [adcChan0.value, adcChan1.value, adcChan2.value, adcChan3.value]
            except OSError as e:
                adc_errors.error(e)  # skip this sample, retry at the next interval
            else:
                adc_errors.ok()
                msg = oscbuildparse.OSCMessage("/adc", None, [normalizer0.normalize(raw[0]), normalizer1.normalize(raw[1]), normalizer2.normalize(raw[2]), normalizer3.normalize(raw[3])])
                osc_send(msg, "client")
                if print_osc:
                    print(msg)
    
    # You can send OSC messages from your event loop too…
    osc_process()
    
# Properly close the system.
osc_terminate()