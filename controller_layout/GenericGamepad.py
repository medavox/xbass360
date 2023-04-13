from enum import Enum, auto


class ControllerButtons(Enum):
    pass

class FACE_BUTTON_NORTH(ControllerButtons):
    pass
class FACE_BUTTON_SOUTH(ControllerButtons):
    pass
class FACE_BUTTON_EAST(ControllerButtons):
    pass
class FACE_BUTTON_WEST(ControllerButtons):
    pass

class DPAD_UP(ControllerButtons):
    pass
class DPAD_DOWN(ControllerButtons):
    pass
class DPAD_LEFT(ControllerButtons):
    pass
class DPAD_RIGHT(ControllerButtons):
    pass

class LEFT_ANALOGUE_STICK_BUTTON(ControllerButtons):
    pass
class RIGHT_ANALOGUE_STICK_BUTTON(ControllerButtons):
    pass

class LEFT_TRIGGER(ControllerButtons):
    pass
class RIGHT_TRIGGER(ControllerButtons):
    pass

# L1 on Playstation, LB on Xbox
class LEFT_SHOULDER_BUTTON(ControllerButtons):
    pass
class RIGHT_SHOULDER_BUTTON(ControllerButtons):
    pass

# eg select on PS1,2; and back on Xbox360
class LEFT_CENTRAL_BUTTON(ControllerButtons):
    pass
# start on Ps1,2 and Xbox 360
class RIGHT_CENTRAL_BUTTON(ControllerButtons):
    pass


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