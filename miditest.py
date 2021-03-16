#!/usr/bin/env python3
import mido
import rtmidi

mido.set_backend('mido.backends.rtmidi')
print("outports:")
print(mido.get_output_names())
print("inports:")
print(mido.get_input_names())

mido.get_output_names()