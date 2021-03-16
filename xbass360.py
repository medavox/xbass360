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
import math
import rtmidi

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

# Init pygame and set it as mido's MIDI backend.
pygame.init()
pygame.joystick.init()
#mido.set_backend('mido.backends.pygame')
mido.set_backend('mido.backends.rtmidi')
print(mido.get_output_names())

deadzone_size = 0.4

outport = mido.open_output(name='LoopBe Internal MIDI 1')


# Show program window.
# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("xBass360")



# Used to manage how fast the screen updates.
clock = pygame.time.Clock()


# Loop until the user clicks the close button.
done = False

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

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

def beyond_deadzone(x, y):
    return math.sqrt(x * x + y * y) > deadzone_size

lastJoystickCount = 0
joystick = None

screen.fill(WHITE)
pygame.display.flip()
# Main program loop.
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if pygame.joystick.get_count():
            if not lastJoystickCount:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
        


            #midi note 21 (A0) is the lowest note in our range: a step below the low B on a 5-string bass
            notes = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
            noteNames = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
            # Detect button presses.
            if event.type == pygame.JOYAXISMOTION:
                screen.fill(WHITE)
                textPrint.reset()
                lx = joystick.get_axis(0)
                ly = joystick.get_axis(1)
                rx = joystick.get_axis(2)
                ry = joystick.get_axis(3)
                ltrigger = joystick.get_axis(4)
                rtrigger = joystick.get_axis(5)

                if beyond_deadzone(lx, ly):
                    vel = math.floor(((ltrigger + 1) / 2.0) * 127)
                    noteIndex = convertXYtoDirection(lx, ly)
                    noteToPlay = notes[noteIndex]
                    textPrint.tprint(screen, "playing note: "+str(noteNames[noteIndex])+" at velocity "+str(vel))
                    outport.send(mido.Message('note_on', note=noteToPlay, velocity=vel))
                # elif ltrigger < -0.999 or not beyond_deadzone(lx, ly):
                #     outport.send(mido.Message('note_off'))#, velocity=vel))
                #textPrint.tprint(screen, "Number of joysticks: {}".format("squelch"))

        lastJoystickCount = pygame.joystick.get_count()
    pygame.display.flip()
    clock.tick(20)

outport.reset()
outport.close()
pygame.quit()
