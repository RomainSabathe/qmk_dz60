# Layers
 
[screenshots]

# Instructions

## How to flash the keyboard & use the layout

(key, or the pins)

## How to update layers.json

(use the gui, update the url and the content)

## How to update the list of supported keys

(play with convert_json.py)

# Specificities

## Shift as a dedicated layer

reason, use

## "Magic key" to change between layouts

- how it works (held --> uses the "other" layer, tapped --> switch to colemak)
- how it's implemented: process_record_user. see https://github.com/qmk/qmk_firmware/blob/master/docs/custom_quantum_functions.md#custom-keycodes

# To extend

- Azerty on the magic key?

# Resources

- [Technical sheet of the ATmega32U4
  chip](http://ww1.microchip.com/downloads/en/devicedoc/atmel-7766-8-bit-avr-atmega16u4-32u4_datasheet.pdf),
  see page 3. The reset pin is at location 13 and a convenient GND pin is at
  location 43.

# Dependencies (Linux)

- Sending Unicode characters requires [IBus](https://wiki.archlinux.org/index.php/IBus#Installation) to be running on your system. Make sure it is running all the time!
- One dependency I was lacking was [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html) (`pip install PyGObject --user`)

# Other bits
