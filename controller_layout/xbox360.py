from GenericGamepad import ControllerButtons as Controller
from GenericGamepad import ControllerAxes as Axes
from GenericGamepad import *

xbox360_controller_buttons = {
    11: Controller.DPAD_UP,
    12: Controller.DPAD_DOWN,
    13: Controller.DPAD_LEFT,
    14: Controller.DPAD_RIGHT,

    0: Controller.FACE_BUTTON_SOUTH,
    3: Controller.FACE_BUTTON_NORTH,
    2: Controller.FACE_BUTTON_WEST,
    1: Controller.FACE_BUTTON_EAST,

    8: Controller.LEFT_ANALOGUE_STICK_BUTTON,
    9: Controller.RIGHT_ANALOGUE_STICK_BUTTON,
    4: Controller.LEFT_SHOULDER_BUTTON,
    5: Controller.RIGHT_SHOULDER_BUTTON,

    6: Controller.LEFT_CENTRAL_BUTTON,
    7: Controller.RIGHT_CENTRAL_BUTTON
}

xbox360_controller_axes = {

    # negative is left, positive is right
    0: Axes.LEFT_ANALOGUE_STICK_X,

    # negative is up, positive is down
    1: Axes.LEFT_ANALOGUE_STICK_Y,

    # negative is left, positive is right
    2: Axes.RIGHT_ANALOGUE_STICK_X,

    # negative is up, positive is down
    3: Axes.RIGHT_ANALOGUE_STICK_Y,
}

hat_to_dpad_map = {
    (1, 0): Controller.DPAD_RIGHT,
    (0, -1): Controller.DPAD_DOWN,
    (-1, 0): Controller.DPAD_LEFT,
    (0, 1):  Controller.DPAD_UP
}


class Xbox360ControllerEventMapper(GamepadPyEventMapper):
    def __init__(self, listener: GenericGamepadListener):
        self.lastHat = {}
        self.listener = listener

    def handleHatMotion(self, axis_num: int, value: tuple[int, int]):
        if self.lastHat[axis_num] is not None:
            if self.lastHat[axis_num][0] != value[0]:
                if self.lastHat[axis_num][0] == 1:
                    self.listener.onButtonUp(Controller.DPAD_RIGHT)
                if self.lastHat[axis_num][0] == -1:
                    self.listener.onButtonUp()
        self.lastHat = {axis_num: value}