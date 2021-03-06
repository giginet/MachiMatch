# -*- coding: utf-8 -*-
#
#    Created on 2011/05/03
#    Created by giginet
#
import settings
import random
from pygame.locals import *
from pywaz.core.game import Game
from pywaz.device import Device
from pywaz.device.joypad import JoyPad
from pywaz.device.key import Key
from main.panel import Panel
from main.roads import *
from main.city import City

class Player(Panel):
    u"""プレイヤークラス"""
    IMAGEPATH = u"../resources/image/main/players.png"
    KEYMAPPINGS = {Device.Key:{'up':K_UP,
                               'down':K_DOWN,
                               'right':K_RIGHT,
                               'left':K_LEFT,
                               'z':K_z,
                               'x':K_x,
                               'c':K_c,
                               'START':K_RETURN
                               },
                   Device.JoyPad:{'up':0,
                                  'down':1,
                                  'right':2,
                                  'left':3,
                                  'z':8,
                                  'x':9,
                                  'c':11,
                                  'START':4
                                  }}
    PAD_TYPE = [0, 0, 0, 1]
    KEYMAPPINGS_PADS = [{'up':0,
                        'down':1,
                        'right':2,
                        'left':3,
                        'z':8,
                        'x':9,
                        'c':11,
                        'START':4
                        },
                        {'up':0,
                        'down':1,
                        'right':7,
                        'left':6,
                        'z':6,
                        'x':7,
                        'c':1,
                        'START':9
                        }]
    def __init__(self, number, world):
        u"""
            number : Player番号。0~3
            world  : Worldクラスインスタンス
        """
        self.number = number
        super(Player, self).__init__(0, 0)
        self.index = self.number
        self.roads_queue = self._get_initial_roads_queue()
        self.current_road = self.get_next_road()
        self.next_road = self.get_next_road()
        self.cursor_counter_h = 0
        self.cursor_counter_v = 0
        self.city = City(self, world)
        self.device = JoyPad(number)
        self.pad_type = self.PAD_TYPE[self.device.id]
        self.mapping = self.KEYMAPPINGS_PADS[self.pad_type]
        self.cursor_threshold = [0, 0]
        self.cursor_move = False
        self.ainfo.index = self.number
        self.point = self.city.root_point.clone()
    def update(self):
        self.city.update()
        if self.pad_type == 0:
            xaxis = self.device.get_axis(0)
            yaxis = self.device.get_axis(1)
        else:
            xaxis = self.device.get_axis(2)
            yaxis = self.device.get_axis(3)    
        length = sum(map(lambda x: x*x, list(self.cursor_threshold)))
        if abs(xaxis) > 0.5:
            self.cursor_threshold[0] += xaxis
            if not self.cursor_move or abs(length) > 16:
                self.point.x += 1 if xaxis > 0 else -1
        if abs(yaxis) > 0.5:
            self.cursor_threshold[1] += yaxis
            if not self.cursor_move or abs(length) > 16:
                self.point.y += 1 if yaxis > 0 else -1
        if abs(xaxis) > 0.5 or abs(yaxis) > 0.5:
            self.cursor_move = True
        else:
            self.cursor_move = False
            self.cursor_threshold = [0, 0]
        if self.point.x < 0:
            self.point.x = 0
        elif self.point.x > settings.STAGE_WIDTH-1:
            self.point.x = settings.STAGE_WIDTH-1
        if self.point.y < 0:
            self.point.y = 0
        elif self.point.y > settings.STAGE_HEIGHT-1:
            self.point.y = settings.STAGE_HEIGHT-1
        self.current_road.point = self.point.clone()
        if not self.device.joy: return
    def draw(self, surface=Game.get_screen()):
        super(Player, self).draw(surface)
        self.city.draw()
    def poll(self):
        self.device.poll()
        if self.device.is_press(self.mapping['z']):
            return -1
        elif self.device.is_press(self.mapping['x']):
            return 1
        elif self.device.is_press(self.mapping['c']):
            return 2 
        elif self.device.is_press(self.mapping['START']):
            return 3
        return 0
    def get_next_road(self):
        if len(self.roads_queue) == 0:
            self.roads_queue = self._get_initial_roads_queue()
        return self.roads_queue.pop(0)(0, 0)
    def _get_initial_roads_queue(self):
        roads = [LShapeRoad, TShapeRoad, IShapeRoad, CrossRoad]
        random.shuffle(roads)
        return roads
    def attach_road(self):
        self.current_road.on_attach()
        self.current_road = self.next_road
        self.current_road.point = self.point
        self.next_road = self.get_next_road()  