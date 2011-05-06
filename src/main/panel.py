# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#
import pygame
import settings
from pywaz.core.game import Game
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.utils.vector import Vector

class Panel(Animation):
    u"""
        パネルクラス。マップ上に存在するもの全てのスーパークラス
        マップ上に存在するものは全てpointというVectorクラスオブジェクトを持つ。
        point(0,0)が画面右上。そこから左下方向にy軸、右下方向にx軸
        抽象クラスなのでインスタンス化してはいけない
    """
    IMAGEPATH = None
    MAXFRAME = 1
    def __init__(self, x, y):
        self.point = Vector(x, y)
        super(Panel, self).__init__(self.IMAGEPATH, AnimationInfo(0, 0, self.MAXFRAME, settings.PANELSIZE, settings.PANELSIZE, 1))
        self.animation_enable = False
    def draw(self, surface=Game.get_screen()):
        if self.point.x < 0:
            self.point.x = 0
        elif self.point.x >= settings.STAGE_WIDTH:
            self.point.x = settings.STAGE_WIDTH-1
        if self.point.y < 0:
            self.point.y = 0
        elif self.point.y >= settings.STAGE_HEIGHT:
            self.point.y = settings.STAGE_HEIGHT-1
        self.x = settings.ROOTX - self.point.y*37 + self.point.x*37
        self.y = settings.ROOTY + self.point.x*19 + self.point.y*19
        super(Panel, self).draw(surface)
    def update(self):
        raise NotImplementedError
    def is_road(self):
        u"""このパネルが道かどうか"""
        return False
    @property
    def surface_center(self):
        u"""パネル表面の中心座標を取り出す"""
        return Vector(self.x+36, self.y+32)
    @property
    def surface_above_edge(self):
        return Vector(self.x+55, self.y+23)
    @property
    def surface_right_edge(self):
        return Vector(self.x+55, self.y+41)
    @property
    def surface_bottom_edge(self):
        return Vector(self.x+18, self.y+43)
    @property
    def surface_left_edge(self):
        return Vector(self.x+24, self.y+24)