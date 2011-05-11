# -*- coding: utf-8 -*-
#
#    Created on 2011/05/10
#    Created by giginet
#

import settings
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.sprite.number import Number

class Navigation(Image):
    NAVIGATION_POSITIONS = ((0,0), (settings.SCREENWIDTH-settings.NAVIGATION_WIDTH, 0), 
                            (0, settings.SCREENHEIGHT-settings.NAVIGATION_HEIGHT), 
                            (settings.SCREENWIDTH-settings.NAVIGATION_WIDTH, settings.SCREENHEIGHT-settings.NAVIGATION_HEIGHT)) # 各プレイヤーごとのナビゲーション表示位置
    #　以下、各プレイヤーごとのパーツ表示位置（相対位置）
    LABEL_POSITIONS = 0
    def __init__(self, owner):
        u"""
            owner : Playerクラスインスタンス
        """
        super(Navigation, self).__init__(u"../resources/image/main/navigation/navigation%d.png" % owner.number)
        self.owner = owner
        self.x, self.y = self.NAVIGATION_POSITIONS[self.owner.number]
        self.label = Image(u"../resources/image/main/navigation/population.png")
        self.label.x = self.x
        self.label.y = self.y
        self.population = Number(u"../resources/image/main/navigation/number.png", w=18, h=45)
        self.population.x = self.label.x + 20
        self.population.y = self.label.y + 20
    def draw(self, surface=Game.get_screen()):
        super(Navigation, self).draw()
        self.label.draw()
        self.population.draw()
    def update(self):
        self.population.n = self.owner.city.population