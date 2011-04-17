# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from pygame.locals import *
from ..utils.singleton import Singleton

class Mouse(Singleton):
    show = True
    
    def __init__(self):
        raise NotImplementedError
    
    @staticmethod
    def is_press(key):
        MOUSENAME = {'LEFT':0,
                 'CENTER':1,
                 'RIGHT':2
        }
        return pygame.mouse.get_pressed()[MOUSENAME[key]]
    
    @staticmethod
    def get_pos():
        return pygame.mouse.get_pos()
    
    @classmethod
    def show_cursor(cls):
        if not cls.show:
            pygame.mouse.set_visible(True)
            cls.show = True
        
    @classmethod
    def hide_cursor(cls):
        if cls.show:
            pygame.mouse.set_visible(False)
            cls.show = False
        
    @staticmethod
    def is_release(self):
        for i in xrange(3):
            if pygame.mouse.get_pressed()[i]:
                return False
        return True