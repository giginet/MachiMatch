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
    IMAGEWIDTH = settings.PANELSIZE
    IMAGEHEIGHT = settings.PANELSIZE
    APF = 1
    def __init__(self, x, y):
        u"""x,y マップ座標"""
        self.point = Vector(x, y)
        super(Panel, self).__init__(self.IMAGEPATH, AnimationInfo(0, 0, self.MAXFRAME, self.IMAGEWIDTH, self.IMAGEHEIGHT, self.APF))
        self.x = settings.ROOT_POSITION[0] - self.point.y*37 + self.point.x*37
        self.y = settings.ROOT_POSITION[1] + self.point.x*19 + self.point.y*19
        self.animation_enable = False
    def draw(self, surface=Game.get_screen(), x=None, y=None):
        u"""
            x, y　: 渡されたとき、その座標に描画。渡されていないときはself.pointを元に算出
        """
        if not x:
            self.x = settings.ROOT_POSITION[0] - self.point.y*37 + self.point.x*37
        else:
            self.x = x
        if not y:
            self.y = settings.ROOT_POSITION[1] + self.point.x*19 + self.point.y*19
        else:
            self.y = y
        super(Panel, self).draw(surface)
    def update(self):
        raise NotImplementedError