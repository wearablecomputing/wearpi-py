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

7. Solder and wire the ADS1115, jack sockets, and the blue potentiometers to the Pi Proto Board as shown in the picture. 

| ![IMG_2981.jpeg](images/IMG_2981.jpeg) | ![IMG_2980.jpeg](images/IMG_2980.jpeg) |
| -------------------- | -------------------- |

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
