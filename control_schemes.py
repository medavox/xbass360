#!/usr/bin/env python3
import common
import pygame.joystick
from common import TextPrint
import mido
import math

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


class DroneBuilder(ControllerScheme):
    textPrint = None

    def __init__(self, screen, textPrint:TextPrint, outputport: mido.ports.BaseOutput):
        super().__init__(screen, textPrint, outputport)
        self.lastPlayedNote = 0
        self.lastVelocity = -1
        self.octave_harmony = False
        self.fifth_harmony = False

    def process_event(self, event, joystick):
        if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
            self.octave_harmony = joystick.get_button(6)
            self.fifth_harmony = joystick.get_button(7)

            #self.outport.send(mido.Message('control_change', control=11, value=1, channel=3))
            self.screen.fill(WHITE)
            self.textPrint.reset()
            self.textPrint.tprint(self.screen, "squelch")
            noteToPlay = self.buttonsToMidiNotes.get(self.buttonsToNumber(joystick))
            #axis 1 = left stick Y
            vel = int(math.floor(((joystick.get_axis(1) + 1) / -2.0) * 127) + 127)
            if vel != self.lastVelocity and common.beyond_deadzone(0.9, joystick.get_axis(0), joystick.get_axis(1)):
                print("velocity "+str(vel))
                self.lastVelocity = vel
                self.outport.send(mido.Message('control_change', channel=3, control=11, value=vel))
            if noteToPlay is not None:
                # axis 4 = right trigger

                self.textPrint.tprint(self.screen, "playing note: "+str(noteToPlay))
                if self.lastPlayedNote != noteToPlay:
                    self.outport.send(mido.Message('note_off', note=self.lastPlayedNote, channel=3))
                    self.lastPlayedNote = noteToPlay
                    print("playing note: "+str(noteToPlay)+" at velocity "+str(vel))
                    self.outport.send(mido.Message('note_on', note=noteToPlay, channel=3, velocity=120))
                    if self.octave_harmony:
                        self.outport.send(mido.Message('note_on', note=noteToPlay, channel=3, velocity=120))
                #print("trigger "+str(joystick.get_axis(5)))

            elif not joystick.get_button(4):#only release notes when left bumper isn't pressed down
                self.outport.send(mido.Message('note_off', note=self.lastPlayedNote, channel=3))
                self.lastPlayedNote = 0

    def buttonsToNumber(self, controller: pygame.joystick.Joystick) -> int:
        ret = 0
        if controller.get_button(0):#a
            ret = ret + 1
        if controller.get_button(1):#b
            ret = ret + 2
        if controller.get_button(2):#x
            ret = ret + 4
        if controller.get_button(3):#y
            ret = ret + 8
        if controller.get_button(5):#right bumper
            ret = ret + 16
        return ret

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

    def octave_select(self, controller: pygame.joystick.Joystick) -> int:
        hat = controller.get_hat(0)
