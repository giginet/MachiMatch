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

class Cave(Building):
    IMAGEPATH = u"../resources/image/main/buildings/cave.png"
    IMAGEWIDTH = 100
    IMAGEHEIGHT = 100
    LEVEL = 1
    OFFSET = (15, 30)

class Home1(Building):
    IMAGEPATH = u"../resources/image/main/buildings/home1.png"
    IMAGEWIDTH = 100
    IMAGEHEIGHT = 100
    LEVEL = 1
    OFFSET = (15, 30)

class Home2(Building):
    IMAGEPATH = u"../resources/image/main/buildings/home2.png"
    IMAGEWIDTH = 100
    IMAGEHEIGHT = 100
    LEVEL = 1
    OFFSET = (15, 30)

    
class WoodCabin(Building):
    IMAGEPATH = u"../resources/image/main/buildings/woodcabin.png"
    LEVEL = 2
    OFFSET = (0, 25)

class BuildingWhite(Building):
    IMAGEPATH = u"../resources/image/main/buildings/building_white.png"
    IMAGEWIDTH = 150
    IMAGEHEIGHT = 200
    LEVEL = 3
    OFFSET = (40, 100)

class BuildingBrown(Building):
    IMAGEPATH = u"../resources/image/main/buildings/building_brown.png"
    IMAGEWIDTH = 150
    IMAGEHEIGHT = 200
    LEVEL = 3
    OFFSET = (40, 100)
    
class Tower(Building):
    IMAGEPATH = u"../resources/image/main/buildings/tower.png"
    IMAGEWIDTH = 200
    IMAGEHEIGHT = 350
    LEVEL = 4
    OFFSET = (60, 250)    
    
class Wheel(Building):
    IMAGEPATH = u"../resources/image/main/buildings/wheel.png"
    IMAGEWIDTH = 150
    IMAGEHEIGHT = 200
    LEVEL = 4
    OFFSET = (30, 120)

class SkyScraper(Building):
    IMAGEPATH = u"../resources/image/main/buildings/skyscraper.png"
    IMAGEWIDTH = 200
    IMAGEHEIGHT = 400
    LEVEL = 4
    OFFSET = (60, 300)
    
class Kawaztan(Building):
    IMAGEPATH = u"../resources/image/main/buildings/kawaztan.png"
    IMAGEWIDTH = 150
    IMAGEHEIGHT = 250
    LEVEL = 4
    OFFSET = (40, 150)
    
class Castle(Building):
    IMAGEPATH = u"../resources/image/main/buildings/castle.png"
    IMAGEWIDTH = 280
    IMAGEHEIGHT = 320
    LEVEL = 5
    OFFSET = (100, 165)

class OrientalCastle(Building):
    IMAGEPATH = u"../resources/image/main/buildings/oriental.png"
    IMAGEWIDTH = 300
    IMAGEHEIGHT = 350
    LEVEL = 5
    OFFSET = (110, 170)

class Babel(Building):
    IMAGEPATH = u"../resources/image/main/buildings/babel.png"
    IMAGEWIDTH = 220
    IMAGEHEIGHT = 280
    LEVEL = 5
    OFFSET = (75, 130)

LEVEL_BUILDINGS = ((Tent, Cave, ), 
                   (WoodCabin, Home1, Home2),
                   (BuildingWhite, BuildingBrown,),
                   (Kawaztan, SkyScraper, Wheel, Tower ),
                   (Babel, Castle, ))