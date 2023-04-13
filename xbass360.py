#!/usr/bin/env python3
"""Use an Xbox 360 controller as a Duophonic MIDI Bass instrument.

This program takes inputs from an Xbox 360 controller and outputs
MIDI messages derived from these inputs.
"""

import os
import sys
import platform
import toml
import mido
import mido.backends.pygame
import pygame
import math
import rtmidi
from common import TextPrint
import control_schemes
from control_schemes import *

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# Init pygame and set it as mido's MIDI backend.
pygame.init()
pygame.joystick.init()
#mido.set_backend('mido.backends.pygame')
mido.set_backend('mido.backends.rtmidi')
print(mido.get_output_names())

outport = mido.open_output(name='loopMIDI Port 1')
#outport = mido.open_output(name='LoopBe Internal MIDI 1')

# Show program window.
# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("xBass360")

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()


lastJoystickCount = 0
joystick = None

screen.fill(WHITE)
pygame.display.flip()

lastLeftHandNote = 0
lastRightHandNote = 0

control_scheme = DroneBuilder(screen, textPrint, outport)

# Main program loop.
# Loop until the user clicks the close button.
done = False

# only allow specific types of events onto the queue
pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.QUIT,
                          pygame.JOYBUTTONDOWN,
                          pygame.JOYBUTTONUP,
                          pygame.JOYAXISMOTION,
                          pygame.JOYHATMOTION,
                          pygame.JOYDEVICEADDED,
                          pygame.JOYDEVICEREMOVED])
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        elif event.type == pygame.JOYDEVICEREMOVED:
            joystick = None

        if joystick is not None:
            control_scheme.process_event(event, joystick)

    lastJoystickCount = pygame.joystick.get_count()
    pygame.display.flip()
    clock.tick(40)

outport.reset()
outport.close()
pygame.quit()
