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
notes = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
noteNames = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
deadzone = 0.4

class ControllerScheme(object):
    def process_event(self, event, joystick):
        pass

    def __init__(self, screen, textPrint:TextPrint, outputport:mido.ports.BaseOutput):
        self.screen = screen
        self.textPrint = textPrint
        self.outport = outputport


class Faces(ControllerScheme):

    #the number is the facebutton bitfield (button combo) that needs to be pressed, and its index in this array is the same as the note that it corresponds to
    faceButtonsToNotes = [0, 1, 5, 4, 12, 8, 10, 2, 3, 7, 15, 14]

    def __init__(self, screen, textPrint:TextPrint, outputport: mido.ports.BaseOutput):
        super().__init__(screen, textPrint, outputport)
        self.lastPlayedNote = 0

    def faceButtonsToNumber(self, controller) -> int:
        ret = 0
        if controller.get_button(0):#a
            ret = ret + 1
        if controller.get_button(1):#b
            ret = ret + 2
        if controller.get_button(2):#x
            ret = ret + 4
        if controller.get_button(3):#y
            ret = ret + 8
        return ret

    def process_event(self, event, joystick):
        if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
            self.screen.fill(WHITE)
            self.textPrint.reset()
            
            lx = joystick.get_axis(0)
            ly = joystick.get_axis(1)
            rx = joystick.get_axis(2)
            ry = joystick.get_axis(3)

            l_bumper = joystick.get_button(4)
            r_bumper = joystick.get_button(5)
            l_stick_btn = joystick.get_button(8)
            r_stick_btn = joystick.get_button(9)
            l_trigger = joystick.get_axis(4)
            r_trigger = joystick.get_axis(5)

            combo = self.faceButtonsToNumber(joystick)
            if combo in self.faceButtonsToNotes:
                noteIndex = self.faceButtonsToNotes.index(combo)
                noteToPlay = notes[noteIndex]
                vel = math.floor(((l_trigger + 1) / 2.0) * 127)
                #play an octave up if the stick button is pushed in
                if l_bumper:
                    noteToPlay = noteToPlay + 24
                if r_bumper:
                    noteToPlay = noteToPlay + 12
                self.textPrint.tprint(self.screen, "playing note: "+str(noteNames[noteIndex])+" at velocity "+str(vel))
                if self.lastPlayedNote != noteToPlay:
                    self.outport.send(mido.Message('note_off', note=self.lastPlayedNote))
                    self.outport.send(mido.Message('control_change', control=7, value=vel))
                    self.lastPlayedNote = noteToPlay
                self.outport.send(mido.Message('note_on', note=noteToPlay, velocity=vel))


class Rotary(ControllerScheme):

    def __init__(self, screen, textPrint:TextPrint, outputport: mido.ports.BaseOutput):
        super().__init__(screen, textPrint, outputport)
        self.lastLeftHandNote = 0
        self.lastRightHandNote = 0

    def process_event(self, event, joystick):
        if event.type == pygame.JOYAXISMOTION:
            self.screen.fill(WHITE)
            self.textPrint.reset()

            lx = joystick.get_axis(0)
            ly = joystick.get_axis(1)
            rx = joystick.get_axis(2)
            ry = joystick.get_axis(3)

            l_bumper = joystick.get_button(4)
            r_bumper = joystick.get_button(5)
            l_stick_btn = joystick.get_button(8)
            r_stick_btn = joystick.get_button(9)
            l_trigger = joystick.get_axis(4)
            r_trigger = joystick.get_axis(5)

            noteIndex = common.convertXYtoDirection(lx, ly)
            if common.beyond_deadzone(deadzone, lx, ly):
                self.textPrint.tprint(self.screen, "playing note: "+str(noteNames[noteIndex]))
            if l_stick_btn:
                vel = math.floor(((l_trigger + 1) / 2.0) * 127)
                noteToPlay = notes[noteIndex] +12
                self.textPrint.tprint(self.screen, "playing note: "+str(noteNames[noteIndex])+" at velocity "+str(vel))
                if self.lastLeftHandNote != noteToPlay:
                    self.outport.send(mido.Message('note_off', note=self.lastLeftHandNote, channel=2))
                    self.lastLeftHandNote = noteToPlay
                self.outport.send(mido.Message('note_on', note=noteToPlay,  channel=2))#velocity=vel,
            else:
                self.outport.send(mido.Message('note_off', note=self.lastLeftHandNote, channel=2))

            RnoteIndex = common.convertXYtoDirection(rx, ry)
            if common.beyond_deadzone(deadzone, rx, ry):
                self.textPrint.tprint(self.screen, "playing note: "+str(noteNames[RnoteIndex]))
            if r_stick_btn:
                vel = math.floor(((r_trigger + 1) / 2.0) * 127)
                noteToPlay = notes[RnoteIndex] +24
                self.textPrint.tprint(self.screen, "playing note: "+str(noteNames[RnoteIndex])+" at velocity "+str(vel))
                if self.lastRightHandNote != noteToPlay:
                    self.outport.send(mido.Message('note_off', note=self.lastRightHandNote, channel=3))
                    self.lastRightHandNote = noteToPlay
                self.outport.send(mido.Message('note_on', note=noteToPlay, channel=3))#velocity=vel,
            else:
                self.outport.send(mido.Message('note_off', note=self.lastRightHandNote, channel=3))


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

    def process_event(self, event, joystick):
        self.screen.fill(WHITE)
        self.textPrint.reset()
        #each event can only be one of these, so ordering doesn't matter
        if event.type == pygame.JOYAXISMOTION:
            self.on_axis_motion(joystick, event.axis, event.value)
        elif event.type == pygame.JOYBUTTONDOWN:
            self.on_button_down(joystick, event.button)
        elif event.type == pygame.JOYBUTTONUP:
            self.on_button_up(joystick, event.button)
        elif event.type == pygame.JOYHATMOTION:
            self.on_hat_motion(joystick, event.hat, event.value)


    def release_note(self): # release the note (and its harmonies) that was playing, if there was any
        if self.playing_note is not None: # if a note was already playing, stop it
            print("playing "+str(self.playing_note+(self.octave_select * 12)))
            self.outport.send(mido.Message('note_off', note=self.playing_note+(self.octave_select * 12), channel=3))

            if self.octave_harmony: # stop the octave harmony if that's activated
                self.outport.send(mido.Message('note_off', note=self.playing_note+12+(self.octave_select * 12), channel=3))

            if self.fifth_harmony: # stop the fifth harmony if that's activated
                self.outport.send(mido.Message('note_off', note=self.playing_note+7+(self.octave_select * 12),  channel=3))
            self.playing_note = None

    def play_note(self, new_note):
        # start a new note
        self.playing_note = new_note
        self.outport.send(mido.Message('note_on', note=new_note+(self.octave_select * 12), channel=3, velocity=120))
        if self.octave_harmony: # play the octave harmony is activated
            self.outport.send(mido.Message('note_on', note=new_note+12+(self.octave_select * 12), channel=3, velocity=120))
        if self.fifth_harmony:# # play the fifth harmony is activated
            self.outport.send(mido.Message('note_on', note=new_note+7+(self.octave_select * 12), channel=3, velocity=120))


    def on_button_down(self, joystick, button_number):
        if button_number == Buttons.START:
            self.fifth_harmony = True
            return

        if button_number == Buttons.BACK:
            self.octave_harmony = True
            return

        new_note = self.buttonsToMidiNotes.get(self.buttonsToNumber(joystick))
        if new_note is not None and new_note != self.playing_note: # if the new button combo is a note, and the note changed
            self.release_note()
            self.play_note(new_note) # play that note




    def on_button_up(self, joystick, button_number):
        if button_number == Buttons.START:
            self.fifth_harmony = False
            return
        if button_number == Buttons.BACK:
            self.octave_harmony = False
            return
        #notelock (not sending not_off when LB is held down)
        #MUST be processed here, where we know which button was just released.
        # so to be consistent, it makes sense to have all the midi command called i nthese methods
        new_note = self.buttonsToMidiNotes.get(self.buttonsToNumber(joystick))
        if new_note is None and not joystick.get_button(Buttons.LB) and button_number != Buttons.LB: # if LB isn't depressed and there was already a note playing AND the button being released isn't the hold button itself, release that note
            self.release_note()

    def on_axis_motion(self, joystick, axis, value):
        # axis 1 = left stick Y
        #use the position of the left stick's Y axis as expression, but only if the stick is >90% from centre
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
                self.play_note(self.playing_note) # but with the new octave
            else:
                self.octave_select = octave


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
