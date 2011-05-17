# -*- coding: utf-8 -*-
#
#    Created on 2011/05/09
#    Created by giginet
#
import settings
from pywaz.core.game import Game
from pywaz.utils.timer import Timer
from main.panel import Panel

class Building(Panel):
    u"""建物クラス"""
    LEVEL = 0
    OFFSET = (0, 0)
    def __init__(self, x, y):
        u"""
            x, y : マップ座標
        """
        self.timer = Timer(settings.FPS*settings.EXTINCT_BUILDING_YEAR)
        self.level = self.LEVEL
        self.timer.play()
        super(Building, self).__init__(x, y)
    def draw(self, surface=Game.get_screen()):
        self.x = settings.ROOT_POSITION[0] - self.point.y*37 + self.point.x*37 - self.OFFSET[0]
        self.y = settings.ROOT_POSITION[1] + self.point.x*19 + self.point.y*19 - self.OFFSET[1]
        super(Panel, self).draw(surface)
    def update(self):
        u"""建物が消えるとき、-1を返す"""
        self.timer.tick()
        if self.timer.is_over():
            return -1
        return 0
    @property
    def size(self):
        if self.level <= 2:
            return 1
        elif self.level <= 4:
            return 2
        else:
            return 4
        
class Tent(Building):
    IMAGEPATH = u"../resources/image/main/buildings/tent.png"
    LEVEL = 1
    OFFSET = (0, 25)
    
class WoodCabin(Building):
    IMAGEPATH = u"../resources/image/main/buildings/woodcabin.png"
    LEVEL = 2
    OFFSET = (0, 25)
    
LEVEL_BUILDINGS = ((Tent,), 
                   (WoodCabin,),
                   (),
                   (),
                   ())