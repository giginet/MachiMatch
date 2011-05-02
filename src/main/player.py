# -*- coding: utf-8 -*-
#
#    Created on 2011/05/03
#    Created by giginet
#
import settings
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.device.joypad import JoyPad
from main.panel import Panel

class Player(Panel):
    u"""プレイヤークラス"""
    IMAGEPATH = u"../resources/image/main/player0.png"
    def __init__(self, number):
        self.number = number
        super(Player, self).__init__(0, 0)
        self.index = self.number
        self.joy = JoyPad().sticks[number]
    def update(self):
        # ToDo　操作性が悪いのであとで改善する
        xaxis = self.joy.get_axis(0)
        yaxis = self.joy.get_axis(1)
        if abs(xaxis) > 0.5:
            self.point.x += 1 if xaxis > 0 else -1
        if abs(yaxis) > 0.5:
            self.point.y += 1 if yaxis > 0 else -1