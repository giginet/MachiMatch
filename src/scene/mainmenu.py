# -*- coding: utf-8 -*-
#
#    Created on 2011/04/17
#    Created by giginet
#
import pygame
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

import os.path
import time
import sys # for debug

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
    
    # �J�[�\����x������dir_x�Ay������dir_y����������
    def set_cursor_pos(self, dir_x, dir_y):
        target_option = False
        while not target_option:
            # y����
            self.cursor_logical_y += dir_y
            if self.cursor_logical_y < 0:
                self.cursor_logical_y += len(self.options)
            if self.cursor_logical_y >= len(self.options):
                self.cursor_logical_y -= len(self.options)
            
            # x����
            self.cursor_logical_x += dir_x
            if self.cursor_logical_x < 0:
                self.cursor_logical_x += len(self.options[self.cursor_logical_y])
            if self.cursor_logical_x >= len(self.options[self.cursor_logical_y]):
                self.cursor_logical_x -= len(self.options[self.cursor_logical_y])
            
            # �`��ʒu�̌v�Z
            target_option = self.options[self.cursor_logical_y][self.cursor_logical_x]
            # �����ŁA�w�肵���ʒu�ɑI�������Ȃ������ꍇ�A
            # ������x�J�[�\���̈ړ���K�p����B�Ⴆ��
            # [Option1] [Option2] [Option3]
            # [Option4]           [Option6]
            # �Ƃ������тŁA[Option4]�ɃJ�[�\���������ԂŉE�L�[��
            # �������Ƃ���B���̂Ƃ��A�J�[�\���͈�x[Option4]��[Option6]��
            # �Ԃɍs�����Ƃ��邪�A���ꂪ�����Ɣ��f����A������x
            # �J�[�\�����E�ɓ����i���ʁA[Option6]�ŃJ�[�\�����~�܂�j�B
        
        # �w�肵���ʒu�ɑI�������������ꍇ�ɁA�͂��߂�while���[�v�𔲂���B
        # �����ŃJ�[�\���̕`��ʒu���v�Z�B
        self.cursor.x = target_option.x - self.CURSOR_BORDER
        self.cursor.y = target_option.y - self.CURSOR_BORDER
    
    # �Q�[�����n�߂�
    def start_game(self, player_number):
        # TODO: �����ɁA�Q�[����ʂֈړ�����R�[�h������
        pass
    
    def ready(self, *args, **kwargs):
        super(MainMenuScene, self).ready()
        
        self.joypads = JoyPad().sticks
        
        self.logo = Image(os.path.join(self.IMAGE_PATH, "kawaz.png"), alpha=False)
        self.config = Image(os.path.join(self.IMAGE_PATH, "config.png"), alpha=False)
        self.exit = Image(os.path.join(self.IMAGE_PATH, "exit.png"), alpha=False)
        self.cursor = Image(os.path.join(self.IMAGE_PATH, "cursor.png"), alpha=True)
        self.load_player_selection(len(self.joypads))
        
        self.logo.x = 353; self.logo.y = 260
        self.player2.x = 160; self.player2.y = 400
        self.player3.x = 380; self.player3.y = 400
        self.player4.x = 600; self.player4.y = 400
        self.config.x  = 380; self.config.y  = 460
        self.exit.x    = 600; self.exit.y    = 460
        # �J�[�\���ʒu��������
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
        
        # last_press_key: �e�v���C���[���A���Ō�ɃL�[����������
        # - X: �Q�[���p�b�hID�iself.joypads (= JoyPad().sticks)�̉��Ԗڂ̃Q�[���p�b�h���j
        #      ��X == len(self.joypads) �̂Ƃ��́A�L�[�{�[�h��\��
        # - Y: �L�[�̖��O
        # * �Q�[���p�b�hX�̃L�[Y�������ꂽ�ꍇ�A
        #   last_press_key[X][Y] = time.time() �Ƃ���B
        # * �Q�[���p�b�hX�̃L�[Y�������ꂽ�ꍇ�A
        #   last_press_key[X].pop(Y) �Ƃ���B
        # * �Q�[���p�b�hX�̃L�[Y��������Ă��邩�́A
        #   Y in last_press_key[X] �Œ��ׂ���B
        # * self.try_pressing_key(keyname, joypad_id) ���Ăяo���ƁA
        #   * �Ō��keyname�̃L�[�������Ă����莞�Ԉȏ�o���Ă���΁A
        #     ���̃L�[���Ō�ɉ������������X�V���ATrue��Ԃ��i�L�[���������Ƃ݂Ȃ��j�B
        #   * �����łȂ����False��Ԃ��i�L�[�������Ȃ������Ƃ݂Ȃ��j�B
        self.last_press_key = [{}]
        for dummy in self.joypads:
            self.last_press_key.append({})
    
    def try_pressing_key(self, keyname, joypad_id):
        time_now = time.time()
        if (keyname not in self.last_press_key[joypad_id]) or (time_now - self.last_press_key[joypad_id][keyname] >= self.KEY_REPEAT_TIME):
            # �L�[���������ꍇ
            self.last_press_key[joypad_id][keyname] = time_now
            return True
        
        # �L�[�������Ȃ������ꍇ
        return False
    
    def update(self):
        # Joypad�ɂ��J�[�\������
        # �eJoypad�ɂ��ē������`�F�b�N����
        for joypad_id in range(len(self.joypads)):
            # ���߂̃L�[���삩��
            xaxis = self.joypads[joypad_id].get_axis(0)
            yaxis = self.joypads[joypad_id].get_axis(1)
            time_now = time.time()
            if xaxis > 0.9:
                if self.try_pressing_key(K_RIGHT, joypad_id):
                    self.set_cursor_pos(1, 0)
            elif xaxis < -0.9:
                if self.try_pressing_key(K_LEFT, joypad_id):
                    self.set_cursor_pos(-1, 0)
            elif yaxis > 0.9:
                if self.try_pressing_key(K_DOWN, joypad_id):
                    self.set_cursor_pos(0, 1)
            elif yaxis < -0.9:
                if self.try_pressing_key(K_UP, joypad_id):
                    self.set_cursor_pos(0, -1)
            
            # �{�^��
            for button_id in range(self.joypads[joypad_id].get_numbuttons()):
                if self.joypads[joypad_id].get_button(button_id):
                    self.actions[self.cursor_logical_y][self.cursor_logical_x]()
        
        # �L�[�{�[�h�ɂ��J�[�\������
        if Key.is_press(K_RIGHT):
            if self.try_pressing_key(K_RIGHT, len(self.joypads)):
                self.set_cursor_pos(1, 0)
        elif Key.is_press(K_LEFT):
            if self.try_pressing_key(K_LEFT, len(self.joypads)):
                self.set_cursor_pos(-1, 0)
        elif Key.is_press(K_DOWN):
            if self.try_pressing_key(K_DOWN, len(self.joypads)):
                self.set_cursor_pos(0, 1)
        elif Key.is_press(K_UP):
            if self.try_pressing_key(K_UP, len(self.joypads)):
                self.set_cursor_pos(0, -1)
        elif Key.is_press(K_RETURN):
            self.actions[self.cursor_logical_y][self.cursor_logical_x]()