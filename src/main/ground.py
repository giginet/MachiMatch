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
    def is_road(self):
        u"""この床が道かどうか"""
        return False
    def is_territory(self):
        u"""この床が領土かどうか"""
        return False
    @property
    def surface_center(self):
        u"""パネル表面の中心座標を取り出す"""
        return Vector(self.x+36, self.y+32)
    @property
    def surface_above_edge(self):
        u"""パネル表面上方中央の座標を取り出す"""
        return Vector(self.x+55, self.y+23)
    @property
    def surface_right_edge(self):
        u"""パネル表面右中央の座標を取り出す"""
        return Vector(self.x+55, self.y+41)
    @property
    def surface_bottom_edge(self):
        u"""パネル表面下方中央の座標を取り出す"""
        return Vector(self.x+18, self.y+43)
    @property
    def surface_left_edge(self):
        u"""パネル表面左中央の座標を取り出す"""
        return Vector(self.x+24, self.y+24)
    def is_connect_with(self, ground):
        u"""指定したgroundと接続されているかどうか"""
        subx = ground.point.x - self.point.x
        suby = ground.point.y - self.point.y
        if suby == -1:
            return self.up and ground.down
        elif subx == 1:
            return self.right and ground.left
        elif suby == 1:
            return self.down and ground.up
        elif subx == -1:
            return self.left and ground.right
        else:
            return False
class Territory(Ground):
    u"""領土クラス"""
    NODE = "1111"
    IMAGEPATH = u"../resources/image/main/chips/ground.png"
    def __init__(self, x, y, owner):
        u"""
            owner : この領土を所持するPlayer
        """
        super(Territory, self).__init__(x, y)
        self.owner = owner
    def is_territory(self):
        return True
class Dummy(Ground):
    u"""ダミーの地形クラス。_mapマトリックス外にアクセスしたときに返される"""
    NODE = "1111"
    def draw(self, surface=Game.get_screen()): pass
    def update(self): pass