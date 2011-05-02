# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#

from main.panel import Panel

class Road(Panel):
    def __init__(self, x, y): 
        self.angle = 0
        super(Road, self).__init__(x, y)
    def rotate(self):
        pass
class LShapeRoad(Road): 
    NODE = 1100
    IMAGEPATH = "../resouces/image/main/chips/chipM.png"
class FlipLShapeRoad(Road): 
    NODE = 1001
class IShapeRoad(Road): 
    NODE = 1010
class TShapeRoad(Road): 
    NODE = 0111
class CrossRoad(Road): 
    NODE = 1111