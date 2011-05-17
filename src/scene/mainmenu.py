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
    CURSOR_BORDER = 10 # カーソルを表す画像が、選択肢を表す画像からどれだけずらして配置されるか
    IMAGE_PATH = "../resources/image/menu"
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
            # ここで、指定した位置に選択肢がなかった場合、
            # もう一度カーソルの移動を適用する。例えば
            # [Option1] [Option2] [Option3]
            # [Option4]           [Option6]
            # という並びで、[Option4]にカーソルがある状態で右キーを
            # 押したとする。このとき、カーソルは一度[Option4]と[Option6]の
            # 間に行こうとするが、それが無効と判断され、もう一度
            # カーソルが右に動く（結果、[Option6]でカーソルが止まる）。
        
        # 指定した位置に選択肢があった場合に、はじめてwhileループを抜ける。
        # ここでカーソルの描画位置を計算。
        self.cursor.x = target_option.x - self.CURSOR_BORDER
        self.cursor.y = target_option.y - self.CURSOR_BORDER
    
    # ゲームを始める
    def start_game(self, player_number):
        # TODO: ここに、ゲーム画面へ移動するコードを書く
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
        
        self.sprites.add(self.logo)
        self.sprites.add(self.player2)
        self.sprites.add(self.player3)
        self.sprites.add(self.player4)
        self.sprites.add(self.config)
        self.sprites.add(self.exit)
        self.sprites.add(self.cursor)
        
        # last_press_key: 各プレイヤーが、いつ最後にキーを押したか
        # - X: ゲームパッドID（self.joypads (= JoyPad().sticks)の何番目のゲームパッドか）
        #      ※X == len(self.joypads) のときは、キーボードを表す
        # - Y: キーの名前
        # * ゲームパッドXのキーYが押された場合、
        #   last_press_key[X][Y] = time.time() とする。
        # * ゲームパッドXのキーYが離された場合、
        #   last_press_key[X].pop(Y) とする。
        # * ゲームパッドXのキーYが押されているかは、
        #   Y in last_press_key[X] で調べられる。
        # * self.try_pressing_key(keyname, joypad_id) を呼び出すと、
        #   * 最後にkeynameのキーを押してから一定時間以上経っていれば、
        #     そのキーを最後に押した時刻を更新し、Trueを返す（キーを押せたとみなす）。
        #   * そうでなければFalseを返す（キーを押せなかったとみなす）。
        self.last_press_key = [{}]
        for dummy in self.joypads:
            self.last_press_key.append({})
    
    def try_pressing_key(self, keyname, joypad_id):
        time_now = time.time()
        if (keyname not in self.last_press_key[joypad_id]) or (time_now - self.last_press_key[joypad_id][keyname] >= self.KEY_REPEAT_TIME):
            # キーを押せた場合
            self.last_press_key[joypad_id][keyname] = time_now
            return True
        
        # キーを押せなかった場合
        return False
    
    def update(self):
        # Joypadによるカーソル操作
        # 各Joypadについて動きをチェックする
        for joypad_id in range(len(self.joypads)):
            # 直近のキー操作から
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
            
            # ボタン
            for button_id in range(self.joypads[joypad_id].get_numbuttons()):
                if self.joypads[joypad_id].get_button(button_id):
                    self.actions[self.cursor_logical_y][self.cursor_logical_x]()
        
        # キーボードによるカーソル操作
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
