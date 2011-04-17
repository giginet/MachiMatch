# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from pygame.locals import *
from ..utils.singleton import Singleton

class Key(Singleton):
    def __init__(self):
        raise NotImplementedError
    
    @classmethod
    def poll(cls):
        cls._keyin = pygame.key.get_pressed()
    
    @classmethod
    def is_press(cls, key):
        return pygame.key.get_focused() and cls._keyin[key]
    
    @classmethod
    def is_release(cls, key):
        return pygame.key.get_focused() and not cls._keyin[key]