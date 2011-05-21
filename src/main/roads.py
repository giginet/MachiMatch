# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#
import settings
from main.ground import Ground
from pywaz.utils.timer import Timer

class Road(Ground):
    def __init__(self, x, y): 
        self.angle = 0
        self.timer = Timer(settings.FPS*settings.EXTINCT_ROAD_YEAR)
        super(Road, self).__init__(x, y)
    def update(self):
        self.timer.tick()
        if self.timer.is_over():
            return 1
    def rotate(self, deg):
        u"""
            deg=1のとき時計回りに、deg=-1のとき反時計回りに回転させる
            self.nodeのbit列を
            右循環シフト＝時計回り
            左循環シフト=反時計回り
        """
        if deg==1:
            self.angle = (self.angle+1)%4
            self.node = (self.node & 1) << 3 | (self.node & 14) >> 1
        elif deg==-1:
            self.angle = (self.angle+3)%4
            self.node = (self.node & 7) << 1 | (self.node & 8) >> 3
    def is_road(self):
        return True
    def on_attach(self):
        self.timer.play()
class LShapeRoad(Road): 
    NODE = "1001"
    IMAGEPATH = "../resources/image/main/roads/LShape.png"
    def rotate(self, deg):
        super(LShapeRoad, self).rotate(deg)
        self.ainfo.frame = self.angle
class IShapeRoad(Road): 
    IMAGEPATH = "../resources/image/main/roads/IShape.png"
    NODE = "0101"
    def rotate(self, deg):
        super(IShapeRoad, self).rotate(deg)
        self.ainfo.frame = self.angle%2
class TShapeRoad(Road): 
    IMAGEPATH = "../resources/image/main/roads/TShape.png"
    NODE = "0111"
    def rotate(self, deg):
        super(TShapeRoad, self).rotate(deg)
        self.ainfo.frame = self.angle
class CrossRoad(Road): 
    IMAGEPATH = "../resources/image/main/roads/Cross.png"
    NODE = "1111"