# wearpi

![wearpi](images/wearpi_2.jpeg)

## Hardware assembly
### Required tools
- Small Phillips head screwdriver
- Soldering iron and solder
- Multimeter
### Instructions
1. Place the Qwiic SHIM on the Raspberry Pi's GPIO header as shown in the picture. Make sure to align the SHIM's Pin 1 with Pin 1 on the Pi's GPIO header as explained [here](https://learn.sparkfun.com/tutorials/qwiic-shim-for-raspberry-pi-hookup-guide?_ga=2.21826875.1846747127.1576523042-1373023627.1571771287), then press it all the way down. ![IMG_4033](images/IMG_4033.jpeg)
2. Connect a 10 cm Qwiic/Stemma QT cable to the socket of the SHIM. 
3. Screw in four 12 mm spacers with sockets on both ends to the four mounting holes of the Pi.
4. Install the HiFiBerry DAC2 ADC Pro audio card on the Pi's GPIO header.
5. Get four 12 mm spacers with a screw on one end and a socket on the other and extend them to 14 mm by screwing in a nut. Screw them in at the four corners of the audio card
6. Drill six 4 mm holes in the Pi Proto Board, circled in red and marked 2 to 7 in the picture on the left. These will be needed for mounting spacers. To get the distances of the holes right place the NanoKey and NanoRotary boards on top of the Proto Board with with the bottom left mounting hole of the NanoKey aligned with mounting hole #1 of the Proto Board, as shown in the picture on the right.

| ![IMG_2980.jpeg](images/IMG_2980.jpeg) | ![IMG_4048.jpeg](images/IMG_4048.jpeg) |
| -------------------- | -------------------- |

7. The circuit on the Proto Board consists of four voltage dividers, one per analogue input of the ADS1115. Solder and wire the ADS1115, jack sockets, and the blue potentiometers to the Pi Proto Board as shown in the picture. Please note that only the side with analogue ins of the ADS1115 is connected to the board using a pin header. For extra safety, you can connect just the pin header to the Proto Board first, complete the rest of the circuit on the back of the board, and finally solder the ADS1115 on the pins. The wiring on the picture below is colour-coded:

| Pin | Colour |
| --- | ------ |
| A-  | Blue   |
| A0  | Purple |
| A1  | Yellow |
| A2  | White  |
| A3  | Orange |
| A+  | Red    |


| ![IMG_2981.jpeg](images/IMG_2981.jpeg) | ![IMG_2980.jpeg](images/IMG_2980.jpeg) |
| -------------------- | -------------------- |

The full circuit is shown in the wiring diagram below, which also covers the Qwiic / STEMMA QT cable chain from steps 10–16. Each channel is a voltage divider. The jack's tip goes to A+. The jack's sleeve goes to the matching ADS1115 input (A0–A3) and to one end of a 500 kΩ trimmer. The trimmer's other end, with its wiper tied to it, goes to A−. The jack's ring is not connected.

Optionally, add a 1 kΩ resistor in series with each trimmer, between the trimmer and A−. It isn't part of the original build, so leave it out (or use a wire link) to reproduce it exactly. It limits the current if a trimmer is turned all the way down while the sensor is pressed hard, which would otherwise short A+ to A−. It will be included on the upcoming custom PCB that replaces the protoboard.

![wearpi wiring diagram](images/wearpi-wiring.svg)

8. Screw in 10 mm spacers in holes you drilled on the Proto Board except for hole #5, in which instead goes a 8 mm spacer.
9. Mount the Proto Board onto the audio card using three screws and one 10 mm spacer on mounting hole #1. 
10. Connect the ADS1115 to the SHIM using the cable you connected in step 2. 
11. Connect key switches and key caps to the NanoKey. You can secure the switches to the board with a bit of hot glue on the back if necessary. 
12. Connect the ADS1115 to the left socket NanoKey using a 4 cm Qwiic/Stemma QT cable.
13. Mount the NanoKey onto the Proto Board by screwing it on spacers # 1, 2 and 7.
14. Solder the encoders to the NanoRotary board and place your favourite knobs on the encoders.
15. Connect the right socket of the NanoKey board to the right socket of the right socket of the NanoRotary board with a 4 cm Qwiic/Stemma QT cable.
16. Connect the left socket of the NanoRotary board to the OLED display to the left socket of the OLED display with a 4 cm Qwiic/Stemma QT cable.
17. Mount the NanoKey board and the OLED board onto the Proto Pi board with four screws on spacers #3, 4, 5 and 6. The OLED board should sit between the NanoKey board and the 8 mm spacer in hole #5, which has the 8 mm spacer.
18. Insert the microSD card flashed with Raspberry OS.
19. Power on the wearpi by connecting a power supply or power bank to the USB-C port. 

## Gallery

| ![IMG_4035.jpeg](images/IMG_4035.jpeg) | ![IMG_4036.jpeg](images/IMG_4036.jpeg) | ![IMG_4037.jpeg](images/IMG_4037.jpeg) |
| ------------------ | ------------------ | ------------------ |
| ![IMG_4038.jpeg](images/IMG_4038.jpeg) | ![IMG_4040.jpeg](images/IMG_4040.jpeg) | ![IMG_4041.jpeg](images/IMG_4041.jpeg) |
| ![IMG_4042.jpeg](images/IMG_4042.jpeg) | ![IMG_4043.jpeg](images/IMG_4043.jpeg) | ![IMG_4044.jpeg](images/IMG_4044.jpeg) |
| ![IMG_4045.jpeg](images/IMG_4045.jpeg) | ![IMG_4046.jpeg](images/IMG_4046.jpeg) | ![wearpi](images/wearpi_2.jpeg) |


## Documentation links

### Breakout boards

#### ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier - STEMMA QT / Qwiic
- https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython 

#### Adafruit I2C Quad Rotary Encoder Breakout
- https://learn.adafruit.com/adafruit-i2c-quad-rotary-encoder-breakout/circuitpython-and-python 

#### Adafruit NeoKey 1x4 QT I2C Breakout
- https://learn.adafruit.com/neokey-1x4-qt-i2c/python-circuitpython 

### OSC

#### Osc4py3
- https://osc4py3.readthedocs.io/en/latest/

## Startup script

The startup script that launches the Python scripts and Pd patches on boot can be found in `shell/startup.sh`. It:

1. Kills any stale instances of the Python OSC scripts, Pd and the MIDI watcher (useful when re-running it by hand). The kill patterns match the exact process names/paths, so they don't hit unrelated commands that merely mention them.
2. Starts the Python OSC scripts (`wearpi-osc-lists-adc-norm-smooth-4in.py` and `wearpi-osc-lists-controls.py`). Their output, including any error tracebacks, goes to `/tmp/wearpi-adc.log` and `/tmp/wearpi-controls.log` (cleared on reboot), together with timestamped start and exit lines. If a script dies, the exit line shows how, e.g. `exited with code 1` for a Python error (see the traceback above it) or `exited with code 132 (SIGILL)` for a crash.
3. Launches the Pd patch in `-nogui` mode. To use a different patch, comment/uncomment the `puredata` lines.
4. Starts the MIDI watcher (`shell/midi-watcher.sh`) in the background, see below.

To run it on startup do the following from the terminal:

- `crontab -e` to edit the crontab file
- Add a line like this at the end of the file: `@reboot /home/wearpi/git/wearpi-py/shell/startup.sh` (make sure the path to the file is correct)
- Ensure the scripts are executable: `chmod +x shell/startup.sh shell/midi-watcher.sh`

### MIDI watcher (EAVI BLE-MIDI board)

The EAVI biosignal board (Bluetooth name `OWL-BioSignals-P010`) sends its data over Bluetooth LE MIDI as 14-bit pitch bends. EAVI input N arrives on MIDI channel N+1 (inputs 1–4 → channels 2–5). BlueZ exposes the board as an ALSA MIDI port, which has to be connected to Pd's MIDI input.

That connection is lost whenever the EAVI reconnects (switched off, battery, out of range) or Pd restarts, because both come back as new ALSA clients. `shell/midi-watcher.sh` takes care of this:

- Every second it tries `aconnect` from the EAVI's port to `Pure Data:0`. This only succeeds when both ports exist and aren't connected yet, so it re-links them within about a second of either one (re)appearing, and does nothing otherwise.
- Ports are matched by name, not number, since ALSA client numbers can change. Both `OWL-BioSignals-P010` and `bluenrg` (the board's internal name, which it has also reported) are tried.
- After each connect it checks that the EAVI is **bonded** and logs a warning if not (see pairing below).
- Every (re)connection is logged with a timestamp to `/tmp/midi-watcher.log` (cleared on reboot). Check it with `cat /tmp/midi-watcher.log`.

If you open a second Pd (e.g. with the GUI) while the startup Pd is running, the watcher only connects the first one. Either stop the startup Pd first (`pkill -x puredata`) or connect manually with `aconnect 'OWL-BioSignals-P010:0' <Pd client number>:0` (find the number with `aconnect -l`).

`pd/test/eavi-bend-test.pd` shows the incoming EAVI data per input (raw value, slider, normalised value, message rate), handy to check the connection.

#### Pairing the EAVI (one time)

The EAVI only sends MIDI over an encrypted connection, so it must be paired with its passkey. If it isn't (or the bond is lost, e.g. after pairing the EAVI with another computer), it still shows as connected and gets a MIDI port, but **no data arrives** and the connection drops every ~30 s. To pair:

```
bluetoothctl
remove E2:16:01:30:31:30     # only if it was added before
scan on                      # wait for OWL-BioSignals-P010 to appear
scan off
pair E2:16:01:30:31:30       # enter the EAVI's passkey when asked
trust E2:16:01:30:31:30      # lets BlueZ reconnect it automatically
connect E2:16:01:30:31:30
quit
```

`bluetoothctl info E2:16:01:30:31:30` should then show `Paired: yes`, `Bonded: yes` and `Trusted: yes`. The bond is stored, so this survives reboots.
