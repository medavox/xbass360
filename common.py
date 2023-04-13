#!/usr/bin/env python3
import math
import pygame

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the information.
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


# how far from the centre does the analogue stick have to be for it to count?
# the controller I tested on had resting values of up to 0.26,
# but higher values may also help reduce false positives when moving between notes
deadzone_size = 0.4


# adapted from https://blackdoor.github.io/blog/thumbstick-controls/
def getAngleFromXY(XAxisValue: float, YAxisValue: float) -> float:
    # Normally Atan2 takes Y,X, not X,Y.  We switch these around since we want 0
    # degrees to be straight up, not to the right like the unit circle;
    angleInRadians = math.atan2(XAxisValue, YAxisValue * -1)

    # Atan2 gives us a negative value for angles in the 3rd and 4th quadrants.
    # We want a full 360 degrees, so we will add 2 PI to negative values.
    if angleInRadians < 0.0:
        angleInRadians = angleInRadians + (math.pi * 2.0)

    # Convert the radians to degrees.  Degrees are easier to visualize.
    angleInDegrees = 180.0 * angleInRadians / math.pi

    return angleInDegrees


# adapted from https://blackdoor.github.io/blog/thumbstick-controls/

def convertXYtoDirection(x: float, y: float) -> int:
    sectors = 12
    # We have 12 sectors, so get the size of each in degrees.
    sectorSize = 360.0 / sectors

    # We also need the size of half a sector
    halfSectorSize = sectorSize / 2.0

    # First, get the angle using the function above
    thumbstickAngle = getAngleFromXY(x, y)

    # Next, rotate our angle to match the offset of our sectors.
    convertedAngle = thumbstickAngle + halfSectorSize

    # Finally, we get the current direction by dividing the angle
    # by the size of the sectors
    direction = math.floor(convertedAngle / sectorSize)

    # the result directions map as follows:
    # 0 = UP, 1 = UP-RIGHT, 2 = RIGHT ... 7 = UP-LEFT.
    return direction % sectors


def beyond_deadzone(deadzone, x: float, y: float) -> bool:
    return math.sqrt(x * x + y * y) > deadzone
