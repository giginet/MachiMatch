# -*- coding: utf-8 -*-
#
#    Created on 2011/05/03
#    Created by giginet
#
import settings
import random
from pygame.locals import *
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.device.joypad import JoyPad
from pywaz.device.key import Key
from main.panel import Panel
from main.roads import *

class Player(Panel):
    u"""プレイヤークラス"""
    IMAGEPATH = u"../resources/image/main/player0.png"
    def __init__(self, number):
        self.number = number
        super(Player, self).__init__(0, 0)
        self.index = self.number
        self.joy = JoyPad().sticks[number]
        self.roads_queue = self._get_initial_roads_queue()
    def update(self):
        # ToDo　操作性が悪いのであとで改善する
        if Key.is_press(K_RIGHT):
            self.point.x += 1
        if Key.is_press(K_LEFT):
            self.point.x -= 1
        if Key.is_press(K_UP):
            self.point.y -= 1
        if Key.is_press(K_DOWN):
            self.point.y += 1
#       
#        xaxis = self.joy.get_axis(0)
#        yaxis = self.joy.get_axis(1)
#        if abs(xaxis) > 0.5:
#            self.point.x += 1 if xaxis > 0 else -1
#        if abs(yaxis) > 0.5:
#            self.point.y += 1 if yaxis > 0 else -1
    def poll(self):
        #if self.joy.get_button(8):
        #    return 1
        #elif self.joy.get_button(9):
        #    return -1
        if Key.is_press(K_z):
            return 1
        elif Key.is_press(K_x):
            return -1
        return 0
    def get_next_road(self):
        if len(self.next_road) == 0:
            self.roads_queue = self._get_initial_roads_queue()
        return self.roads_queue.pop(0)()
    def _get_initial_roads_queue(self):
        roads = [LShapeRoad, FlipLShapeRoad, TShapeRoad, IShapeRoad, CrossRoad]
        random.shuffle(roads)
        return roads