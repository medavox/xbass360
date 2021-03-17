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
import common
import control_schemes

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

control_scheme = control_schemes.DroneBuilder()

# Main program loop.
# Loop until the user clicks the close button.
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if pygame.joystick.get_count():
            if not lastJoystickCount:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                
                #rotary(event, joystick)
            drone_builder(event, joystick, screen)

    lastJoystickCount = pygame.joystick.get_count()
    pygame.display.flip()
    clock.tick(15)

outport.reset()
outport.close()
pygame.quit()
