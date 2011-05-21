# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
import pygame

from pywaz.device import Device

class JoyPad(Device):
    _type = Device.JoyPad
    pygame.joystick.init()
    
    def __init__(self, id):
        print pygame.joystick.get_count()
        if pygame.joystick.get_count() > id:
            self.joy = pygame.joystick.Joystick(id)
            self.joy.init()
            self.numbuttons = self.joy.get_numbuttons()
        else:
            self.joy = None
            self.numbuttons = 0
        self._enable_repeats = [False] * self.numbuttons
        self._pressed = [False] * self.numbuttons
        self.id = id
    def poll(self):
        for key, pressed in enumerate(self._pressed):
            if pressed and not self.joy.get_button(key):
                self._pressed[key] = False
    def is_press(self, key):
        if not self.joy: return False
        if self._enable_repeats[key] or (not self._enable_repeats[key] and not self._pressed[key]):
            if self.joy.get_button(key):
                self._pressed[key] = True
                return True
        return False
    def get_num_axes(self):
        if not self.joy: return 0
        return self.joy.get_numaxes()
    def get_axis(self, id):
        if not self.joy or id >= self.get_num_axes():
            return 0
        return self.joy.get_axis(id)
    @staticmethod
    def get_num_joypads():
        return pygame.joystick.get_count()
    
    
class DisableJoy(Device):
    def __init__(self, id):
        self.id = id