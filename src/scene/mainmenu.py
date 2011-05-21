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
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.mixer.bgm import BGM
from pywaz.utils.vector import Vector
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse
from pywaz.sprite.button import Button
from pywaz.device.joypad import JoyPad
from pywaz.device.key import Key


class MainMenuScene(Scene):
    BACKGROUND = (255,255,255)
    CURSOR_BORDER = 10 # �J�[�\����\���摜���A�I������\���摜����ǂꂾ�����炵�Ĕz�u����邩
    IMAGE_PATH = "../resources/image/menu"
    KEY_REPEAT_TIME = 0.2 # ���b�ȓ��̊ԂȂ�A�L�[�������ꑱ���Ă��Ă��A�łƂ݂Ȃ��Ȃ���
    
    # 2Players, 3Players, 4Players�̉摜��ǂݍ���
    def load_player_selection(self, joypad_number):
        fail = ("" if joypad_number >= 2 else "x")
        self.player2 = Image(os.path.join(self.IMAGE_PATH, "player2%s.png" % fail), alpha=False)
        
        fail = ("" if joypad_number >= 3 else "x")
        self.player3 = Image(os.path.join(self.IMAGE_PATH, "player3%s.png" % fail), alpha=False)
        
        fail = ("" if joypad_number >= 4 else "x")
        self.player4 = Image(os.path.join(self.IMAGE_PATH, "player4%s.png" % fail), alpha=False)
    
    # �J�[�\����x����dir_x�Ay����dir_y����������
    def set_cursor_pos(self, dir_x, dir_y):
        target_option = False
        while not target_option:
            # y���
            self.cursor_logical_y += dir_y
            if self.cursor_logical_y < 0:
                self.cursor_logical_y += len(self.options)
            if self.cursor_logical_y >= len(self.options):
                self.cursor_logical_y -= len(self.options)
            
            # x���
            self.cursor_logical_x += dir_x
            if self.cursor_logical_x < 0:
                self.cursor_logical_x += len(self.options[self.cursor_logical_y])
            if self.cursor_logical_x >= len(self.options[self.cursor_logical_y]):
                self.cursor_logical_x -= len(self.options[self.cursor_logical_y])
            
            # �`��ʒu�̌v�Z
            target_option = self.options[self.cursor_logical_y][self.cursor_logical_x]
        self.cursor.x = target_option.x - self.CURSOR_BORDER
        self.cursor.y = target_option.y - self.CURSOR_BORDER
    
    # �Q�[�����n�߂�
    def start_game(self, player_number):
        # TODO: �����ɁA�Q�[����ʂֈړ�����R�[�h������
        Game.get_scene_manager().change_scene('game', players=player_number)
        self.bgm.fadeout(100)
    
    def ready(self, *args, **kwargs):
        super(MainMenuScene, self).ready()
        self.bgm = BGM(u'../resources/music/title.mp3', -1)
        self.num_joypads = JoyPad.get_num_joypads()
        self.joypads = [] 
        for i in xrange(0, self.num_joypads):
            self.joypads.append(JoyPad(i))
        self.logo = Image(os.path.join(self.IMAGE_PATH, "kawaz.png"), alpha=False)
        self.config = Image(os.path.join(self.IMAGE_PATH, "config.png"), alpha=False)
        self.exit = Image(os.path.join(self.IMAGE_PATH, "exit.png"), alpha=False)
        self.cursor = Image(os.path.join(self.IMAGE_PATH, "cursor.png"), alpha=True)
        self.cursor_threshold = [[0, 0], ] * self.num_joypads # ジョイスティックを倒したときに、axisがどれくらい倒れたかの総量
        self.cursor_move = [False] * self.num_joypads
        self.load_player_selection(self.num_joypads)
        self.logo.x = 353; self.logo.y = 260
        self.player2.x = 160; self.player2.y = 400
        self.player3.x = 380; self.player3.y = 400
        self.player4.x = 600; self.player4.y = 400
        self.config.x  = 380; self.config.y  = 460
        self.exit.x    = 600; self.exit.y    = 460
        # �J�[�\���ʒu������
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
        self.bgm.play()
        for id, joypad in enumerate(self.joypads):
            xaxis = joypad.get_axis(0)
            yaxis = joypad.get_axis(1)
            length = sum(map(lambda x: x*x, list(self.cursor_threshold[id])))
            if abs(xaxis) > 0.5:
                self.cursor_threshold[id][0] += xaxis
                if not self.cursor_move[id] or abs(length) > 16:
                    self.set_cursor_pos(1 if xaxis > 0 else - 1, 0)
            if abs(yaxis) > 0.5:
                self.cursor_threshold[id][1] += yaxis
                if not self.cursor_move[id] or abs(length) > 16:
                    self.set_cursor_pos(0, 1 if yaxis > 0 else - 1)
            if abs(xaxis) > 0.5 or abs(yaxis) > 0.5:
                self.cursor_move[id] = True
            else:
                self.cursor_move[id] = False
            self.cursor_threshold[id] = [0, 0]
# �{�^��
            if joypad.is_press(11):
                self.actions[self.cursor_logical_y][self.cursor_logical_x]()