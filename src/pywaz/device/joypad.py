# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
import pygame

from pywaz.utils.singleton import Singleton

class JoyPad(Singleton):
    sticks = []
    
    def __init__(self):
        pygame.joystick.init()
        for id in xrange(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(id)
            joy.init()
            self.sticks.append(joy)

    @staticmethod
    def get_count():
        return pygame.joystick.get_count()
            