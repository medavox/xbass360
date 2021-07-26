from enum import Enum, auto


class ControllerButtons(Enum):
    
    FACE_BUTTON_NORTH: str = "FACE_BUTTON_NORTH"
    FACE_BUTTON_SOUTH: str = "FACE_BUTTON_SOUTH"
    FACE_BUTTON_EAST: str = "FACE_BUTTON_EAST"
    FACE_BUTTON_WEST: str = "FACE_BUTTON_WEST"

    DPAD_UP: str = "DPAD_UP"
    DPAD_DOWN: str = "DPAD_DOWN"
    DPAD_LEFT: str = "DPAD_LEFT"
    DPAD_RIGHT: str = "DPAD_RIGHT"

    LEFT_ANALOGUE_STICK_BUTTON: str = "LEFT_ANALOGUE_STICK_BUTTON"
    RIGHT_ANALOGUE_STICK_BUTTON: str = "RIGHT_ANALOGUE_STICK_BUTTON"

    LEFT_TRIGGER: str = "LEFT_TRIGGER"
    RIGHT_TRIGGER: str = "RIGHT_TRIGGER"

    # L1 on Playstation, LB on Xbox
    LEFT_SHOULDER_BUTTON: str = "LEFT_SHOULDER_BUTTON"
    RIGHT_SHOULDER_BUTTON: str = "RIGHT_SHOULDER_BUTTON"

    # eg select on PS1,2; and back on Xbox360
    LEFT_CENTRAL_BUTTON: str = "LEFT_CENTRAL_BUTTON"
    # start on Ps1,2 and Xbox 360
    RIGHT_CENTRAL_BUTTON: str = "RIGHT_CENTRAL_BUTTON"


class ControllerAxes(Enum):

    LEFT_ANALOGUE_STICK_X: str = "LEFT_ANALOGUE_STICK_X"
    LEFT_ANALOGUE_STICK_Y: str = "LEFT_ANALOGUE_STICK_Y"

    RIGHT_ANALOGUE_STICK_X: str = "RIGHT_ANALOGUE_STICK_X"
    RIGHT_ANALOGUE_STICK_Y: str = "RIGHT_ANALOGUE_STICK_Y"


class GamepadPyEventMapper:

    def handleButtonDown(self, button_num: int):
        pass

    def handleButtonUp(self, button_num: int):
        pass

    def handleHatMotion(self, axis_num: int, value: tuple[int, int]):
        pass

    def handleAxisMotion(self, axis_num: int, value: int):
        pass


class GenericGamepadListener:
    def onButtonDown(self, button: ControllerButtons):
        pass

    def onButtonUp(self, button: ControllerButtons):
        pass

    def onAxisMotion(self, axis:ControllerAxes, value:float):
        pass