# -*- coding: utf-8 -*-
#
#    Created on 2011/05/10
#    Created by giginet
#

import settings
from pywaz.sprite.image import Image
from pywaz.sprite.number import Number

class Navigation(object):
    NAVIGATION_POSITIONS = ((0,0), (settings.SCREENWIDTH-settings.NAVIGATION_WIDTH, 0), 
                            (0, settings.SCREENHEIGHT-settings.NAVIGATION_HEIGHT), (settings.SCREENWIDTH-settings.NAVIGATION_WIDTH, settings.SCREENHEIGHT-settings.NAVIGATION_HEIGHT))
    def __init__(self, owner):
        u"""
            owner : Playerクラスインスタンス
        """
        self.owner = owner
        self.background = Image(u"../resources/image/main/navigation/navigation%d.png" % self.owner.number)
        self.background.x, self.background.y = self.NAVIGATION_POSITIONS[self.owner.number]
        self.label = Image(u"../resources/image/main/navigation/population.png")
        self.label.x = self.background.x
        self.label.y = self.background.y
        self.population = Number(u"../resources/image/main/navigation/number.png", w=18, h=45)
        self.population.x = self.label.x + 20
        self.population.y = self.label.y + 20
    def draw(self):
        self.background.draw()
        self.label.draw()
        self.population.draw()
    def update(self):
        self.population.n = self.owner.city.population