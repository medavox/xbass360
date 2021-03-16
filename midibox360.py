#!/usr/bin/env python3
"""Xbox 360 controller to MIDI controller.

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

# Determine config file location.
if platform.system() == 'Windows':
    config_dir = os.environ['LOCALAPPDATA']
else:
    config_dir = os.path.join(os.environ['HOME'], '.config')


# Init pygame and set it as mido's MIDI backend.
pygame.init()
pygame.joystick.init()
mido.set_backend('mido.backends.pygame')
print(mido.get_output_names())

playing_notes = []
octave = 0
playing = 0

# Open output port.
if port == '':
    outport = mido.open_output()
else:
    outport = mido.open_output(port)

# Show program window.
screen = pygame.display.set_mode([320, 180])
pygame.display.set_caption("midiBox360")

if os.path.isfile(logo):
    logo = pygame.image.load(logo)
    screen.blit(logo, (0,0))
    pygame.display.flip()

if pygame.joystick.get_count():
    joystick = pygame.joystick.Joystick(joystick_id)
    joystick.init()

clock = pygame.time.Clock()

done = False

#adapted from https://blackdoor.github.io/blog/thumbstick-controls/
def getAngleFromXY(XAxisValue, YAxisValue):

    #Normally Atan2 takes Y,X, not X,Y.  We switch these around since we want 0
    # degrees to be straight up, not to the right like the unit circle;
    angleInRadians = math.atan2(XAxisValue, YAxisValue * -1)

    #Atan2 gives us a negative value for angles in the 3rd and 4th quadrants.
    # We want a full 360 degrees, so we will add 2 PI to negative values.
    if angleInRadians < 0.0:
        angleInRadians = angleInRadians + (math.pi * 2.0)

    #Convert the radians to degrees.  Degrees are easier to visualize.
    angleInDegrees = 180.0 * angleInRadians / math.pi

    return angleInDegrees

#adapted from https://blackdoor.github.io/blog/thumbstick-controls/
def convertXYtoDirection(X, Y):
    sectors = 12
    #We have 12 sectors, so get the size of each in degrees.
    sectorSize = 360.0 / sectors

    #We also need the size of half a sector
    halfSectorSize = sectorSize / 2.0

    #First, get the angle using the function above
    thumbstickAngle = getAngleFromXY(X, Y)

    #Next, rotate our angle to match the offset of our sectors.
    convertedAngle = thumbstickAngle + halfSectorSize

    #Finally, we get the current direction by dividing the angle
    # by the size of the sectors
    direction = math.floor(convertedAngle / sectorSize)

    #the result directions map as follows:
    # 0 = UP, 1 = UP-RIGHT, 2 = RIGHT ... 7 = UP-LEFT.
    return direction % sectors


# Main program loop.
while done==False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        lx = joystick.get_axis(0)
        ly = joystick.get_axis(1)
        rx = joystick.get_axis(2)
        ry = joystick.get_axis(3)
        leftStickAngle = 180 + math.atan2(ly, lx) / math.pi * 180
        rightStickAngle = 180 +  math.atan2(ry, rx) / math.pi * 180

        # Move base note up or down an octave/semitone.
        if event.type == pygame.JOYHATMOTION:
            if get_event(hat_up):
                base_note = (base_note + 12) % 128
            if get_event(hat_down):
                base_note = (base_note - 12) % 128
            if get_event(hat_left):
                base_note = (base_note - 1) % 128
            if get_event(hat_right):
                base_note = (base_note + 1) % 128
#midi note 21 (A0) is the lowest note in our range: a step below the low B on a 5-string bass
        # Detect button presses.
        if event.type == pygame.JOYBUTTONDOWN:
        if event.type == pygame.JOYBUTTONUP:
            if not root():
                # Release all notes.
                playing = False
                while len(playing_notes) > 0:
                    outport.send(mido.Message('note_off',
                                channel=channel, note=playing_notes.pop()))

    clock.tick(30)

outport.reset()
outport.close()
pygame.quit()
