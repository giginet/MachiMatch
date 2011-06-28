# -*- coding: utf-8 -*-
#
#    Created on 2011/04/17
#    Created by giginet
#
import pygame
import os.path
import sys # for debug

import settings
from pygame.locals import *

from pywaz.scene.abstractscene import Scene
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.mixer.bgm import BGM
from pywaz.mixer.sound import Sound
from pywaz.device.joypad import JoyPad
from pywaz.utils.timer import Timer

class MainMenuScene(Scene):
    BACKGROUND = (255,255,255)
    CURSOR_BORDER = 10 # カーソルを表す画像が、選択肢を表す画像からどれだけずらして配置されるか
    IMAGE_PATH = r"../resources/image/menu"
    KEY_REPEAT_TIME = 0.2 # 何秒以内の間なら、キーが押され続けていても連打とみなさないか
    
    # 2Players, 3Players, 4Playersの画像を読み込む
    def load_player_selection(self, joypad_number):
        fail = ("" if joypad_number >= 2 else "x")
        self.player2 = Image(os.path.join(self.IMAGE_PATH, "player2%s.png" % fail), alpha=False)
        
        fail = ("" if joypad_number >= 3 else "x")
        self.player3 = Image(os.path.join(self.IMAGE_PATH, "player3%s.png" % fail), alpha=False)
        
        fail = ("" if joypad_number >= 4 else "x")
        self.player4 = Image(os.path.join(self.IMAGE_PATH, "player4%s.png" % fail), alpha=False)
    
    # カーソルをx方向にdir_x、y方向にdir_yだけ動かす
    def set_cursor_pos(self, dir_x, dir_y):
        target_option = False
        while not target_option:
            # y方向
            self.cursor_logical_y += dir_y
            if self.cursor_logical_y < 0:
                self.cursor_logical_y += len(self.options)
            if self.cursor_logical_y >= len(self.options):
                self.cursor_logical_y -= len(self.options)
            
            # x方向
            self.cursor_logical_x += dir_x
            if self.cursor_logical_x < 0:
                self.cursor_logical_x += len(self.options[self.cursor_logical_y])
            if self.cursor_logical_x >= len(self.options[self.cursor_logical_y]):
                self.cursor_logical_x -= len(self.options[self.cursor_logical_y])
            
            # 描画位置の計算
            target_option = self.options[self.cursor_logical_y][self.cursor_logical_x]
        self.cursor.x = target_option.x - self.CURSOR_BORDER
        self.cursor.y = target_option.y - self.CURSOR_BORDER
    # ゲームを始める
    def start_game(self, player_number):
        self.decide_timer.play()
        self.decide_sound.play()
        self.player_number = player_number
    def ready(self, *args, **kwargs):
        super(MainMenuScene, self).ready()
        self.bgm = BGM(u'../resources/music/title.wav', -1)
        self.cursor_sound = Sound("../resources/sound/cursor.wav")
        self.decide_sound = Sound('../resources/sound/decide.wav')
        self.decide_timer = Timer(settings.FPS*2.5)
        self.num_joypads = JoyPad.get_num_joypads()
        self.joypads = [] 
        for i in xrange(0, self.num_joypads):
            self.joypads.append(JoyPad(i))
        self.background = Image(os.path.join(self.IMAGE_PATH, "background3.png"), alpha=False)
        self.logo = Image(os.path.join(self.IMAGE_PATH, "logo.png"))
        self.config = Image(os.path.join(self.IMAGE_PATH, "config.png"), alpha=False)
        self.exit = Image(os.path.join(self.IMAGE_PATH, "exit.png"), alpha=False)
        self.cursor = Image(os.path.join(self.IMAGE_PATH, "cursor.png"), alpha=True)
        self.cursor_threshold = [[0, 0], ] * self.num_joypads # ジョイスティックを倒したときに、axisがどれくらい倒れたかの総量
        self.cursor_move = [False] * self.num_joypads
        self.load_player_selection(self.num_joypads)
        self.logo.x = 280; self.logo.y = 20
        self.player2.x = 160; self.player2.y = 400
        self.player3.x = 380; self.player3.y = 400
        self.player4.x = 600; self.player4.y = 400
        self.config.x  = 380; self.config.y  = 460
        self.exit.x    = 600; self.exit.y    = 460
        # カーソル位置を初期化
        self.options = ((self.player2, self.player3, self.player4),
                        (None, self.config, self.exit))
        self.actions = ((lambda:self.start_game(2), # self.player2
                         lambda:self.start_game(3), # self.player3
                         lambda:self.start_game(4),)# self.player4
                       ,
                        (lambda:0, # None
                         lambda:Game.get_scene_manager().change_scene('keysetting'), #self.config
                         lambda:sys.exit()) # self.exit
                       )
        self.cursor_logical_x = 0;
        self.cursor_logical_y = 0;
        self.set_cursor_pos(0, 0)
        self.sprites.add(self.background)
        self.sprites.add(self.logo)
        self.sprites.add(self.player2)
        self.sprites.add(self.player3)
        self.sprites.add(self.player4)
        self.sprites.add(self.config)
        self.sprites.add(self.exit)
        self.sprites.add(self.cursor)
        
        self.last_press_key = [{}]
        for dummy in self.joypads:
            self.last_press_key.append({})
    
    def update(self):
        self.decide_timer.tick()
        if self.decide_timer.is_over():
            Game.get_scene_manager().change_scene('game', players=self.player_number)
            self.bgm.fadeout(100)
        if self.decide_timer.is_active(): return
        self.bgm.play()
        for id, joypad in enumerate(self.joypads):
            xaxis = joypad.get_axis(0)
            yaxis = joypad.get_axis(1)
            length = sum(map(lambda x: x*x, list(self.cursor_threshold[id])))
            if abs(xaxis) > 0.5:
                self.cursor_threshold[id][0] += xaxis
                if not self.cursor_move[id] or abs(length) > 16:
                    self.cursor_sound.play()
                    self.set_cursor_pos(1 if xaxis > 0 else - 1, 0)
            if abs(yaxis) > 0.5:
                self.cursor_threshold[id][1] += yaxis
                if not self.cursor_move[id] or abs(length) > 16:
                    self.cursor_sound.play()
                    self.set_cursor_pos(0, 1 if yaxis > 0 else - 1)
            if abs(xaxis) > 0.5 or abs(yaxis) > 0.5:
                self.cursor_move[id] = True
            else:
                self.cursor_move[id] = False
            self.cursor_threshold[id] = [0, 0]
            if joypad.is_press(11):
                self.actions[self.cursor_logical_y][self.cursor_logical_x]()
