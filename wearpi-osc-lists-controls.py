import board
import digitalio
import time

import adafruit_seesaw.digitalio
import adafruit_seesaw.rotaryio
import adafruit_seesaw.seesaw

from adafruit_neokey.neokey1x4 import NeoKey1x4

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse


def log(message):
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}")


class I2CErrorReporter:
    """Rate-limited reporting of I2C read errors.

    A single failed I2C read (e.g. OSError [Errno 121] Remote I/O error from a
    loose cable or noise on the bus) should not kill the script: the caller
    skips that cycle and retries. This class logs the first failure, then a
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
            log(f"{self.name}: I2C read failed ({e}), skipping and retrying")
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


print_osc = False
ip = "127.0.0.1"
port = 57121

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client(ip, port, "client")

# use default I2C bus
i2c = board.I2C()

def init_with_retry(fn, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            print(f"Init attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    raise RuntimeError(f"Failed to initialise after {retries} attempts")

# Create a NeoKey object
neokey = init_with_retry(lambda: NeoKey1x4(i2c, addr=0x30))

seesaw = init_with_retry(lambda: adafruit_seesaw.seesaw.Seesaw(i2c, 0x49))

encoders = [adafruit_seesaw.rotaryio.IncrementalEncoder(seesaw, n) for n in range(4)]
switches = [adafruit_seesaw.digitalio.DigitalIO(seesaw, pin) for pin in (12, 14, 17, 9)]
for switch in switches:
    switch.switch_to_input(digitalio.Pull.UP)  # input & pullup!

last_positions = [0, 0, 0, 0]
enc_rot = [0, 0, 0, 0]
last_enc_button = [True, True, True, True]

last_button = [False, False, False, False]

last_time = 0

i2c_errors = I2CErrorReporter("controls (encoders/NeoKey)")

print("Starting controls loop \n")
# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:

    # Read all I2C inputs first, so a failed read skips the whole cycle
    # instead of leaving the state half-updated.
    try:
        positions = [encoder.position for encoder in encoders]
        switch_vals = [switch.value for switch in switches]
        key_vals = [neokey[n] for n in range(4)]
    except OSError as e:
        i2c_errors.error(e)
        time.sleep(0.01)  # don't hammer a failing bus
        osc_process()
        continue
    i2c_errors.ok()

    # read encoders
    changed = False
    for n, rotary_pos in enumerate(positions):
        if rotary_pos != last_positions[n]:
            changed = True
            if rotary_pos > last_positions[n]: 
                enc_rot[n] = 1
            else:
                if rotary_pos < last_positions[n]:
                    enc_rot[n] = -1
            last_positions[n] = rotary_pos
        else:
            enc_rot[n] = 0
            
    if changed:
        msg = oscbuildparse.OSCMessage("/enc-rot", None, enc_rot)
        osc_send(msg, "client")
        if print_osc:
            print(msg)

    changed = False
    for n, enc_button in enumerate(switch_vals):
        if enc_button != last_enc_button[n]:
            last_enc_button[n] = enc_button
            changed = True
            
    if changed:
        enc_but = [int(not button) for button in switch_vals]
        msg = oscbuildparse.OSCMessage("/enc-but", None, enc_but)
        osc_send(msg, "client")
        if print_osc:
            print(msg)
#read buttons
    changed = False
    for n, button_val in enumerate(key_vals):
        if button_val != last_button[n]:
            changed = True
        last_button[n] = button_val
    if changed:
        keys = [int(key) for key in key_vals]
        msg = oscbuildparse.OSCMessage("/key", None, keys)
        osc_send(msg, "client")
        if print_osc:
            print(msg)


    # You can send OSC messages from your event loop too…
    osc_process()
    

# Properly close the system.
osc_terminate()