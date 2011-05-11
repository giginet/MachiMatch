# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#

from pywaz.sprite.image import Image

import numbers
import pygame
import settings

from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.sprite import OrderedUpdates
from pywaz.sprite.image import Image
from pywaz.core.game import Game

class Number(Sprite):
    def __init__(self, filepath, n=0, x=0, y=0, w=20, h=40, offset=0):
        super(Number, self).__init__()
        self.width = w
        self.height = h
        self.offset = offset
        self.n = int(n)
        self.pre_n = self.n
        self.x = x
        self.y = y
        self.filepath = filepath
        self._parse()
        
    def _parse(self):
        place = len(str(self.n))
        self.image = pygame.surface.Surface((self.width*place+self.offset*place, self.height))
        self.image.set_colorkey((0,0,0))
        dest = self.image.get_rect().move(self.x, self.y)
        area = dest
        for i,s in enumerate(str(self.n)):
            n = int(s)
            image = Image(self.filepath)
            dest = pygame.rect.Rect((self.width+self.offset)*i,0, self.width, self.height)
            area = Rect(n*self.width, 0, self.width, self.height)
            self.image.blit(image.image, dest, area)
    
    def draw(self, surface=Game.get_screen()):
        if self.n != self.pre_n:
            self.pre_n = self.n
            self._parse()
        dest = self.image.get_rect().move(self.x, self.y)
        return surface.blit(self.image, dest=dest)
    
    def get_surface(self):
        return self.image