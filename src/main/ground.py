# -*- coding: utf-8 -*-
#
#    Created on 2011/05/03
#    Created by giginet
#
from pywaz.core.game import Game
from pywaz.utils.vector import Vector
from main.panel import Panel

class Ground(Panel):
    u"""
        地形クラス
        隣の地形と道が繋がるかどうかを2進数表記で保持する
        上右下左の順に=1111
    """
    NODE = "0000"
    IMAGEPATH = u"../resources/image/main/chips/grass.png"
    def __init__(self, x, y):
        self.node = int(self.NODE, 2)
        super(Ground, self).__init__(x, y)
    @property
    def up(self):
        return self.node & 8
    @property
    def right(self):
        return self.node & 4
    @property
    def down(self):
        return self.node & 2
    @property
    def left(self):
        return self.node & 1    
class Territory(Ground):
    u"""領土クラス"""
    NODE = "1111"
    IMAGEPATH = u"../resources/image/main/chips/ground.png"
    def __init__(self, x, y, owner):
        super(Territory, self).__init__(x, y)
        self.owner = owner
class Dummy(Ground):
    u"""ダミーの地形クラス。_mapマトリックス外にアクセスしたときに返される"""
    NODE = "1111"
    def draw(self, surface=Game.get_screen()): pass
    def update(self): pass