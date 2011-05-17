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
    LABEL_POSITIONS = ((10, 0),(170, 0),(10, 0),(170, 0))
    POPULATION_POSITIONS = ((5, 25),(120, 25),(5, 25),(120, 25))
    NEXT_POSITIONS = ((217, 12),(7, 12),(217, 12),(7, 12))
    def __init__(self, owner):
        u"""
            owner : Playerクラスインスタンス
        """
        super(Navigation, self).__init__(u"../resources/image/main/navigation/navigation%d.png" % owner.number)
        self.owner = owner
        number = self.owner.number
        self.x, self.y = self.NAVIGATION_POSITIONS[self.owner.number]
        self.population = PopulationCounter(owner)
        self.population.x = self.x + self.LABEL_POSITIONS[number][0] + self.POPULATION_POSITIONS[number][0]
        self.population.y = self.y + self.LABEL_POSITIONS[number][1] + self.POPULATION_POSITIONS[number][1]
        self.pre_population = self.owner.city.population
        self.pre_next_road = self.owner.next_road.__class__
        if number % 2 ==1:
            self.population.align = Number.TEXTALIGNRIGHT
    def draw(self, surface=Game.get_screen()):
        super(Navigation, self).draw()
        self.population.draw()
        self.owner.next_road.draw(x=self.x+self.NEXT_POSITIONS[self.owner.number][0], 
                                  y=self.y+self.NEXT_POSITIONS[self.owner.number][1]
                                  )
    def update(self):
        self.population.update()
class PopulationCounter(Number):
    u"""人口カウンタ。増える様子をアニメーションさせる"""
    def __init__(self, owner):
        u"""
            owner : Playerクラスインスタンス
        """
        self.owner = owner
        super(PopulationCounter, self).__init__(u"../resources/image/main/navigation/number.png", w=18, h=45)
        self.n = self.owner.city.population
    def update(self):
        population = self.owner.city.population
        if self.n != population:
            sub = abs(population - self.n) # 差
            place = len(str(sub)) # 桁数
            if self.n < population:
                self.n += 10**(place-1) 
            else:
                self.n -= 10**(place-1)
            