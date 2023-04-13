#!/usr/bin/env python3

import pygame
import math
from common import *

# Define some colors.
from TextPrint import TextPrint




# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 900))

pygame.display.set_caption("Controller Test")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit next loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass
        else:
            textPrint.tprint(screen, "GUID: {}".format(guid))

        # Usually axes run in pairs: up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()
        
        lx = joystick.get_axis(0)
        ly = joystick.get_axis(1)
        rx = joystick.get_axis(2)
        ry = joystick.get_axis(3)
        leftStickAngle = 180 + math.atan2(ly, lx) / math.pi * 180
        rightStickAngle = 180 +  math.atan2(ry, rx) / math.pi * 180
        textPrint.tprint(screen, "Left stick angle:: {}".format(getAngleFromXY(lx, ly)))
        textPrint.tprint(screen, "Right stick angle:: {}".format(rightStickAngle))

        
        #the centrepoint angle for each note
        angles = [90, 120, 150, 180, 210, 240, 270, 300, 330, 0, 30, 60]

        notes = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        #the lowest angle considered to be within that note's range
        angle_starts = [75, 105, 135, 155, 185, 215, 245, 275, 305, 335, 5, 35]
        textPrint.tprint(screen, "NOTE:: {}".format(convertXYtoDirection(lx, ly)))
        textPrint.tprint(screen, "left trigger magnitude:: {}".format(math.sqrt(lx * lx + ly * ly)))
        textPrint.tprint(screen, "right trigger magnitude:: {}".format(math.sqrt(rx * rx + ry * ry)))

        # for i in range(0, len(notes)):
        #     if leftStickAngle >= angle_starts[i] and leftStickAngle < angle_starts[(i + 1) % len(angle_starts)]:
        #         textPrint.tprint(screen, "NOTE:: {}".format(notes[i]))
        #         break

    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()