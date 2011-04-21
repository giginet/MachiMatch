# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#

import pygame
import settings
from panel import Panel
from pywaz.sprite import OrderedUpdates

class World(object):
    def __init__(self, *args, **kwargs):
        self.generate_stage()
    def generate_stage(self):
        self._map = []
        self.panels = OrderedUpdates()
        for y in xrange(settings.STAGE_HEIGHT):
            column = []
            for x in xrange(settings.STAGE_WIDTH):
                panel = Panel(x, y)
                column.append(panel)
                self.panels.add(panel)
            self._map.append(column)
    def draw(self):
        for p in self.panels:
            p.x = settings.ROOTX - p.point.y*20 + p.point.x*20
            p.y = settings.ROOTY + p.point.x*10 + p.point.y*10
            p.draw()
        return pygame.rect.Rect(settings.ROOTY, settings.ROOTX-settings.STAGE_HEIGHT*20, 
                                settings.STAGE_HEIGHT*20, settings.STAGE_WIDTH*20)
    def update(self):
        pass