#!/usr/bin/env python3
import common
import pygame.joystick
from common import TextPrint
import mido
import math
import enum

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

#midi note 21 (A0) is the lowest note in our range: a step below the low B on a 5-string bass
deadzone = 0.4

class ControllerScheme(object):
    def process_event(self, event, joystick):
        pass

    def __init__(self, screen, textPrint:TextPrint, outputport:mido.ports.BaseOutput):
        self.screen = screen
        self.textPrint = textPrint
        self.outport = outputport

class Buttons(enum.IntEnum):
    A    = 0
    B    = 1
    X    = 2
    Y    = 3
    LB   = 4
    RB   = 5
    BACK = 6
    START= 7
    LS   = 8
    RS   = 9
    GUIDE=10


class Axes(enum.IntEnum):
    LX = 0
    LY = 1
    RX = 2
    RY = 3
    LT = 4
    RT = 5


class DroneBuilder(ControllerScheme):
    textPrint = None

    def __init__(self, screen, textPrint:TextPrint, outputport: mido.ports.BaseOutput):
        super().__init__(screen, textPrint, outputport)
        self.lastPlayedNote = 0
        self.expression = 0
        self.octave_harmony = False
        self.fifth_harmony = False
        self.playing_note = None
        self.octave_select = 0
        self.state_changed = False

    def process_event(self, event, joystick):
        self.screen.fill(WHITE)
        self.textPrint.reset()
        #each event can only be one of these, so ordering doesn't matter
        if event.type == pygame.JOYAXISMOTION:
            self.on_axis_motion(joystick, event.axis, event.value)
        elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
            self.on_button_change(joystick, event.button, event.type == pygame.JOYBUTTONDOWN)
        elif event.type == pygame.JOYHATMOTION:
            self.on_hat_motion(joystick, event.hat, event.value)
        self.consider_state_change(joystick)

    def consider_state_change(self, joystick):
        if self.state_changed:
            if self.playing_note is not None:
                self.release_note()
            new_note = self.buttonsToMidiNotes.get(self.buttonsToNumber(joystick))
            if new_note is not None:
                self.play_note(new_note)
                self.state_changed = False
            #else:  # new note is None - all notes should be released,


    def release_note(self): # release the note (and its harmonies) that was playing, if there was any
        if self.playing_note is not None:  # if a note was already playing, stop it
            print("playing "+str(self.playing_note+(self.octave_select * 12)))
            self.outport.send(mido.Message('note_off', note=self.playing_note+(self.octave_select * 12), channel=3))

            if self.octave_harmony: # stop the octave harmony if that's activated
                self.outport.send(mido.Message('note_off', note=self.playing_note+12+(self.octave_select * 12), channel=3))

            if self.fifth_harmony: # stop the fifth harmony if that's activated
                self.outport.send(mido.Message('note_off', note=self.playing_note+7+(self.octave_select * 12),  channel=3))
            self.playing_note = None

    def play_note(self, new_note):
        # start a new note
        if new_note != self.playing_note:
            self.playing_note = new_note
        self.outport.send(mido.Message('note_on', note=new_note+(self.octave_select * 12), channel=3, velocity=120))
        if self.octave_harmony: # play the octave harmony is activated
            self.outport.send(mido.Message('note_on', note=new_note+12+(self.octave_select * 12), channel=3, velocity=120))
        if self.fifth_harmony:# # play the fifth harmony is activated
            self.outport.send(mido.Message('note_on', note=new_note+7+(self.octave_select * 12), channel=3, velocity=120))

    def on_button_change(self, joystick, button_number, falseUpTrueDown:bool):
        print("button number: "+str(button_number))
        if button_number == Buttons.START and falseUpTrueDown:
            self.fifth_harmony = not self.fifth_harmony
            print("fifth harmony "+("ENABLED" if self.fifth_harmony else "DISABLED"))
            if not self.fifth_harmony:
                self.outport.send(mido.Message('note_off', note=self.playing_note+7+(self.octave_select * 12),  channel=3))
            else:
                self.state_changed = True

        if button_number == Buttons.BACK and falseUpTrueDown:
            self.octave_harmony = not self.octave_harmony
            print("octave harmony "+("ENABLED" if self.octave_harmony else "DISABLED"))
            if not self.octave_harmony:
                self.outport.send(mido.Message('note_off', note=self.playing_note+12+(self.octave_select * 12), channel=3))
            else:
                self.state_changed = True
        # notelock (not sending note_off when LB is held down) MUST be processed here,
        # where we know which button was just released.
        # so to be consistent, it makes sense to have all the midi command called in these methods
        new_note = self.buttonsToMidiNotes.get(self.buttonsToNumber(joystick))
        if new_note != self.playing_note:
            self.state_changed = True
        # if LB isn't depressed and there was already a note playing AND the button being released isn't the hold button itself, release that note
        #if self.playing_note is not None and not joystick.get_button(Buttons.LB) and button_number != Buttons.LB and falseUpTrueDown is False:
        #    self.release_note()

    def on_axis_motion(self, joystick, axis, value):
        # axis 1 = left stick Y
        # use the position of the left stick's Y axis as expression, but only if the stick is >90% from centre
        if axis == Axes.LY:
            vel = int(math.floor(((value + 1) / -2.0) * 127) + 127)
            if vel != self.expression and common.beyond_deadzone(0.9, joystick.get_axis(Axes.LX), joystick.get_axis(Axes.LY)):
                print("velocity "+str(vel))
                self.expression = vel
                self.outport.send(mido.Message('control_change', channel=3, control=11, value=self.expression))

    def on_hat_motion(self, joystick, hat, value):
        octave = self.octave_map.get(value)
        if octave is not None:
            if octave != self.octave_select:
                self.release_note()
                self.octave_select = octave
                self.state_changed = True

    def buttonsToNumber(self, controller: pygame.joystick.Joystick) -> int:
        ret = 0
        if controller.get_button(Buttons.A):
            ret = ret + 1
        if controller.get_button(Buttons.B):
            ret = ret + 2
        if controller.get_button(Buttons.X):
            ret = ret + 4
        if controller.get_button(Buttons.Y):
            ret = ret + 8
        if controller.get_button(Buttons.RB):
            ret = ret + 16
        return ret

    #up and right are positive
    #(x,y)
    octave_map = {
        (1, 0): 0,
        (0, -1): 1,
        (-1, 0): 2,
        (0, 1):  3
    }

    buttonsToMidiNotes = {
        1 : 21,# a   = A
        5 : 22,# a+x = A#
        4 : 23,# x   = B
        12: 24,# x+y = C
        8 : 25,# y   = C#
        10: 26,# y+b = D
        2 : 27,# b   = D#
        3 : 28,# a+b = E
        #with LB
        17: 28,# a   = E (same E)
        21: 29,# a+x = F
        20: 30,#x    = F#
        28: 31,#x+y  = G
        24: 32,# y   = G#
        26: 33,# y+b = A*(Octave)
        18: 34,# b   = A#*
        19: 35 # a+b = B*
    }
#how about we treat it like the gamespeak from abes odyssey
#L1, L2, R1, R2 are each held as toggles
# press a face button while holding a shoulder button to ring a note
# the shoulder button is the 'pluck' that activates teh noet;
# this leave th possibility of an extra 'open' note sounidng when you press a shoulder button without also presssing a face button
# 16 possibilities
#4 groups of 4 (or 5 if you include the open note)

#get logical state (convert axis data to expression)
#check if different from last state
#if so, cancel previous state
# initiate new state

#what about playing new notes over sustained existing ones?
# might need a (set/stack/queue) of sustained notes

##or.... the sustain idea might have to go
