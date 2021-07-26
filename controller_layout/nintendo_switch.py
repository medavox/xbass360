from GenericGamepad import ControllerButtons as Controller
from GenericGamepad import ControllerAxes as Axes
from GenericGamepad import *

switch_pro_controller_buttons = {
    11: Controller.DPAD_UP,
    12: Controller.DPAD_DOWN,
    13: Controller.DPAD_LEFT,
    14: Controller.DPAD_RIGHT,

    1: Controller.FACE_BUTTON_SOUTH,
    2: Controller.FACE_BUTTON_NORTH,
    3: Controller.FACE_BUTTON_WEST,
    0: Controller.FACE_BUTTON_EAST,

    7: Controller.LEFT_ANALOGUE_STICK_BUTTON,
    8: Controller.RIGHT_ANALOGUE_STICK_BUTTON,
    9: Controller.LEFT_SHOULDER_BUTTON,
    10: Controller.RIGHT_SHOULDER_BUTTON,

    4: Controller.LEFT_CENTRAL_BUTTON,
    6: Controller.RIGHT_CENTRAL_BUTTON
}

switch_pro_controller_axes = {
    0: Axes.LEFT_ANALOGUE_STICK_X,
    1: Axes.LEFT_ANALOGUE_STICK_Y,
    2: Axes.RIGHT_ANALOGUE_STICK_X,
    3: Axes.RIGHT_ANALOGUE_STICK_Y,
}


class SwitchProControllerHandler(GamepadPyEventMapper):

    def __init__(self, listener: GenericGamepadListener):
        self.listener = listener

    def handleButtonDown(self, button_num: int):
        self.listener.onButtonDown(switch_pro_controller_buttons[button_num])

    def handleButtonUp(self, button_num: int):
        self.listener.onButtonDown(switch_pro_controller_buttons[button_num])

    def handleHatMotion(self, axis_num: int, value: tuple[int, int]):
        #TODO

    def handleAxisMotion(self, axis_num: int, value: int):
        #todo: check the axes aren't flipped between xbox and switch, or some shit