# -*- coding: utf-8 -*-
#
#    Created on 2011/05/05
#    Created by giginet
#

import settings
from main.panel import Panel

class Immigrant(Panel):
    u"""移民クラス"""
    def __init__(self, x):
        self.direction = 0 #右上から時計回りに0~3
        super(Immigrant, self).__init__(x, settings.STAGE_HEIGHT-1)
    u"""
        とりあえずマスの真ん中まで進む
        真ん中まで辿り着いたら、その床と周辺の床のnode情報を見て、繋がっているかどうか判定する
        隣のマスが存在しないときは、存在しないマスをnode=1111と扱う
        直進できる場合、直進して次の床へ
        直進できない場合、向かって左右いずれかへランダムに進む
        それもできない場合、進行方向逆向きに進む
    """
    def update(self):
        pass