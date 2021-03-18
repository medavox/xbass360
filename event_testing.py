#!/usr/bin/env python3


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

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# Init pygame
pygame.init()
pygame.joystick.init()


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

# Main program loop.
# Loop until the user clicks the close button.
done = False

# only allow specific types of events onto the queue
pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.QUIT,
                          pygame.JOYBUTTONDOWN,
                          pygame.JOYBUTTONUP,
                          pygame.JOYAXISMOTION,
                          pygame.JOYHATMOTION])
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if pygame.JOYAXISMOTION == event.type:
            print("axis "+str(event.axis)+" motion: "+str(event.value))
        elif pygame.JOYHATMOTION == event.type:
            print("Hat: "+str(event.hat)+"; value: "+str(event.value))
        elif pygame.JOYBUTTONDOWN == event.type:
            print("button down: "+str(event.button))
        else:
            print("event type:"+str(pygame.event.event_name(event.type)))
        if pygame.joystick.get_count():
            if not lastJoystickCount:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()

            pass

    lastJoystickCount = pygame.joystick.get_count()
    pygame.display.flip()
    clock.tick(15)


pygame.quit()
