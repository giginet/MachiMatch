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
from main.city import City

class Player(Panel):
    u"""プレイヤークラス"""
    IMAGEPATH = u"../resources/image/main/player0.png"
    def __init__(self, number, world):
        u"""
            number : Player番号。0~3
            world  : Worldクラスインスタンス
        """
        self.number = number
        super(Player, self).__init__(0, 0)
        self.index = self.number
        #self.joy = JoyPad().sticks[number]
        self.roads_queue = self._get_initial_roads_queue()
        self.current_road = self.get_next_road()
        self.next_road = self.get_next_road()
        self.pressed_attach = False
        self.pressed_rotate_r = False
        self.pressed_rotate_l = False
        self.cursol_counter_h = 0
        self.cursol_counter_v = 0
        self.city = City(number, world)
    def update(self):
        if not self.number == 0: return
        # ToDo　操作性が悪いのであとで改善する
        if Key.is_press(K_RIGHT):
            self.cursol_counter_h += 1
            if self.cursol_counter_h > 1:
                self.cursol_counter_h = 0
                self.point.x += 1
        elif Key.is_press(K_LEFT):
            self.cursol_counter_h += 1
            if self.cursol_counter_h > 1:
                self.cursol_counter_h = 0
                self.point.x -= 1
        else:
            self.cursol_counter_h = 0
        if Key.is_press(K_UP):
            self.cursol_counter_v += 1
            if self.cursol_counter_v > 1:
                self.cursol_counter_v = 0
                self.point.y -= 1
        elif Key.is_press(K_DOWN):
            self.cursol_counter_v += 1
            if self.cursol_counter_v > 1:
                self.cursol_counter_v = 0
                self.point.y += 1
        else:
            self.cursol_counter_v = 0
        if self.point.x < 0:
            self.point.x = 0
        elif self.point.x > settings.STAGE_WIDTH-1:
            self.point.x = settings.STAGE_WIDTH-1
        if self.point.y < 0:
            self.point.y = 0
        elif self.point.y > settings.STAGE_HEIGHT-1:
            self.point.y = settings.STAGE_HEIGHT-1
#
#        xaxis = self.joy.get_axis(0)
#        yaxis = self.joy.get_axis(1)
#        if abs(xaxis) > 0.5:
#            self.point.x += 1 if xaxis > 0 else -1
#        if abs(yaxis) > 0.5:
#            self.point.y += 1 if yaxis > 0 else -1
        self.current_road.point = self.point.clone()
    def poll(self):
        if not self.number == 0: return 0
        return self._poll_key()
    def get_next_road(self):
        if len(self.roads_queue) == 0:
            self.roads_queue = self._get_initial_roads_queue()
        return self.roads_queue.pop(0)(0, 0)
    def _get_initial_roads_queue(self):
        roads = [LShapeRoad, TShapeRoad, IShapeRoad, CrossRoad]
        random.shuffle(roads)
        return roads
    def _poll_key(self):
        if Key.is_press(K_z):
            if not self.pressed_rotate_l: 
                self.pressed_rotate_l = True 
                return -1
        elif Key.is_press(K_x):
            if not self.pressed_rotate_r: 
                self.pressed_rotate_r = True
                return 1
        elif Key.is_press(K_c):
            if not self.pressed_attach:
                self.pressed_attach = True 
                return 2
        else:
            self.pressed_attach = False
            self.pressed_rotate_l = False
            self.pressed_rotate_r = False
        return 0
    def _poll_joypad(self):
        if self.joy.get_button(8):
            if not self.pressed_rotate_l: 
                self.pressed_rotate_l = True 
                return -1
        elif self.joy.get_button(9):
            if not self.pressed_rotate_r: 
                self.pressed_rotate_r = True
                return 1
        elif self.joy.get_button(1):
            if not self.pressed_attach:
                self.pressed_attach = True 
                return 2
        else:
            self.pressed_attach = False
            self.pressed_rotate_l = False
            self.pressed_rotate_r = False
        return 0
    def attach_road(self):
        self.current_road.on_attach()
        self.current_road = self.next_road
        self.current_road.point = self.point
        self.next_road = self.get_next_road()
    