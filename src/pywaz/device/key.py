# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from pygame.locals import *
from pywaz.device import Device

class Key(Device):
    _type = Device.Key
    def __init__(self, id):
        self.id = id
        self._pressed_keys = pygame.key.get_pressed()
        self.numbuttons = len(self._pressed_keys)
        self._enable_repeats = [True] * self.numbuttons
        self._pressed = [False] * self.numbuttons
    def poll(self):
        self._pressed_keys = pygame.key.get_pressed()
        for key, pressed in enumerate(self._pressed):
            if pressed and pygame.key.get_focused() and not self._pressed_keys[key]:
                self._pressed[key] = False
    def is_press(self, key):
        if pygame.key.get_focused() and self._pressed_keys[key]:
            if self._enable_repeats[key] or (not self._enable_repeats[key] and not self._pressed[key]):
                self._pressed[key] = True
                return True
        return False
    def is_release(self, key):
        return pygame.key.get_focused() and not self._pressed_keys[key]
    def enable_repeat(self, key):
        self._enable_repeats[key] = True
    def disable_repeat(self, key):
        self._enable_repeats[key] = False
    def get_repeat(self, key):
        return self._enable_repeats[key]
    def get_num_axes(self):
        return 2
    def get_axis(self, key):
        if key >= 2:
            return 0
        if key == 0:
            if pygame.key.get_focused() and self._pressed_keys[K_UP]:
                return -1
            if pygame.key.get_focused() and self._pressed_keys[K_DOWN]:
                return 1
        elif key == 1:
            if pygame.key.get_focused() and self._pressed_keys[K_LEFT]:
                return -1
            if pygame.key.get_focused() and self._pressed_keys[K_RIGHT]:
                return 1
        return 0