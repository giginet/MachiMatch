# -*- coding: utf-8 -*-
#
#    Created on 2011/05/06
#    Created by giginet
#

import random
import settings
from pywaz.utils.vector import Vector
from main.immigrant import Immigrant

class ImmigrantManager(object):
    u"""移民を管理するクラス"""
    def __init__(self, world):
        u"""
            world: selfを保持するWorldクラスインスタンス
        """
        self.world = world
        self.immigrants = []
    def create_immigrant(self, x):
        u"""x列の一番手前の行に新しく移民を生成する"""
        at = Vector(x, settings.STAGE_HEIGHT-1)
        ground = self.world.get_panel_on(at)
        if not ground.down: return # 道が下に繋がっていなかったら生成しない
        immigrant = Immigrant(x, settings.STAGE_HEIGHT-1, self.world)
        self.immigrants.append(immigrant)
    def remove_immigrant(self, immigrant):
        u"""immigrantをマップ上から削除する"""
        del self.immigrants[self.immigrants.index(immigrant)]
    def update(self):
        map(lambda immigrant: immigrant.update(), self.immigrants)
        r = random.randint(0, 10)
        if r==0:
            x = random.randint(0, settings.STAGE_WIDTH-1)
            self.create_immigrant(x)
    def draw(self):
        map(lambda immigrant: immigrant.draw(), self.immigrants)