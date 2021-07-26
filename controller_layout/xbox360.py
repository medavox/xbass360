from GenericGamepad import ControllerButtons as Controller
from GenericGamepad import ControllerAxes as Axes

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
    0: Axes.LEFT_ANALOGUE_STICK_X,
    1: Axes.LEFT_ANALOGUE_STICK_Y,
    2: Axes.RIGHT_ANALOGUE_STICK_X,
    3: Axes.RIGHT_ANALOGUE_STICK_Y,
}