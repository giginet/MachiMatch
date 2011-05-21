# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from pygame.locals import *
from pywaz.device import Device
from pywaz.utils.vector import Vector

class Mouse(Device):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    numbuttons = 3
    _type = Device.Mouse
    def __init__(self, id):
        self.id = id
    def is_press(self, key):
        return pygame.mouse.get_focused() and pygame.mouse.get_pressed()[key]
    def get_pos(self):
        return Vector(pygame.mouse.get_pos())