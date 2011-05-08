# -*- coding: utf-8 -*-
#
#    Created on 2011/05/05
#    Created by giginet
#
import pygame
import settings
from pywaz.core.game import Game
from pywaz.utils.vector import Vector
from main.panel import Panel

class Immigrant(Panel):
    u"""移民クラス"""
    SPEED = 5
    def __init__(self, x, y, world):
        u"""移民を生成するマップ座標x, y, """
        super(Immigrant, self).__init__(x, y)
        self.direction = 0    #右上から時計回りに0~3
        self.world = world    #ステージ情報を保持しておく
        self.current_panel = self.world.get_panel_on(self.point)   #今いるパネル座標
        self.goal = Vector(self.current_panel.panel_center)  #次に移民が向かう座標
        self.x, self.y = self.current_panel.surface_bottom_edge.to_pos()
    u"""
        とりあえずマスの真ん中まで進む
        真ん中まで辿り着いたら、その床と周辺の床のnode情報を見て、繋がっているかどうか判定する
        隣のマスが存在しないときは、存在しないマスをnode=1111と扱う
        直進できる場合、直進して次の床へ
        直進できない場合、向かって左右いずれかへランダムに進む
        それもできない場合、進行方向逆向きに進む
    """
    def update(self):
        current = Vector(self.x, self.y)
        sub = self.goal - current
        if sub.length < self.SPEED:
            self.x, self.y = self.goal.to_pos()
        else:
            sub = sub.resize(self.SPEED)
            current = current + sub
            self.x, self.y = current.to_pos()
    def draw(self, surface=Game.get_screen()):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), 3)
        return super(Panel, self).draw(surface)