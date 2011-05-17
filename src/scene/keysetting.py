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

class KeySettingScene(Scene):
    BACKGROUND = (255,255,255)
    CURSOR_BORDER = 10 # カーソルを表す画像が、選択肢を表す画像からどれだけずらして配置されるか
    IMAGE_PATH = "../resources/image/menu"
    KEY_REPEAT_TIME = 0.2 # 何秒以内の間なら、キーが押され続けていても連打とみなさないか
    
    def ready(self, *args, **kwargs):
        super(KeySettingScene, self).ready()
        
        self.joypads = JoyPad().sticks
        
        # どのプレイヤーが何のキーの設定をしているか。
        # 0: 方向キーを入力（どのゲームパッドを何プレイヤーが使うか確かめるため）
        # 1: 右回転に使うキー
        # 2: 左回転に使うキー
        # 3: パネルを置くのに使うキー
        # 4: 完了
        self.phase = [0, 0, 0, 0]
        
        # どのプレイヤーがどのゲームパッドを使っているか。
        # （self.joypadsの何番目のゲームパッドを使っているかで指定する）
        # ただし、キーボードで操作するプレイヤーについては-1、
        # 設定が完了していないプレイヤーについてはNoneを指定する。
        self.player2joypad = [None, None, None, None]
        
        # 必要な画像を読み込む
        self.instruction = [{}, {}, {}, {}]
        self.instruction_message = [[], [], [], []]
        for i in range(4):
            y_pos_icons = 120 * i + 10
            self.instruction[i]["phaseicon1"] = Image(os.path.join(self.IMAGE_PATH, "keysetting1.png"), alpha=False)
            self.instruction[i]["phaseicon2"] = Image(os.path.join(self.IMAGE_PATH, "keysetting2.png"), alpha=False)
            self.instruction[i]["phaseicon3"] = Image(os.path.join(self.IMAGE_PATH, "keysetting3.png"), alpha=False)
            self.instruction[i]["phaseicon4"] = Image(os.path.join(self.IMAGE_PATH, "keysetting4.png"), alpha=False)
            self.instruction[i]["arrowicon1"] = Image(os.path.join(self.IMAGE_PATH, "keysetting-arrow.png"), alpha=True)
            self.instruction[i]["arrowicon2"] = Image(os.path.join(self.IMAGE_PATH, "keysetting-arrow.png"), alpha=True)
            self.instruction[i]["arrowicon3"] = Image(os.path.join(self.IMAGE_PATH, "keysetting-arrow.png"), alpha=True)
            self.instruction[i]["phaseicon1"].x = 290
            self.instruction[i]["phaseicon1"].y = y_pos_icons
            self.instruction[i]["phaseicon2"].x = 390
            self.instruction[i]["phaseicon2"].y = y_pos_icons
            self.instruction[i]["phaseicon3"].x = 490
            self.instruction[i]["phaseicon3"].y = y_pos_icons
            self.instruction[i]["phaseicon4"].x = 590
            self.instruction[i]["phaseicon4"].y = y_pos_icons
            self.instruction[i]["arrowicon1"].x = 340
            self.instruction[i]["arrowicon1"].y = y_pos_icons
            self.instruction[i]["arrowicon2"].x = 440
            self.instruction[i]["arrowicon2"].y = y_pos_icons
            self.instruction[i]["arrowicon3"].x = 540
            self.instruction[i]["arrowicon3"].y = y_pos_icons
            
            self.instruction[i]["cursor"] = Image(os.path.join(self.IMAGE_PATH, "cursor-square.png"), alpha=True)
            self.instruction[i]["cursor"].x = self.instruction[i]["phaseicon1"].x - self.CURSOR_BORDER
            self.instruction[i]["cursor"].y = self.instruction[i]["phaseicon1"].y - self.CURSOR_BORDER
            
            self.instruction_message[i].append(Image(os.path.join(self.IMAGE_PATH, "instruction-1-%d.png" % (i + 1)), alpha=False))
            self.instruction_message[i].append(Image(os.path.join(self.IMAGE_PATH, "instruction-2.png"), alpha=False))
            self.instruction_message[i].append(Image(os.path.join(self.IMAGE_PATH, "instruction-3.png"), alpha=False))
            self.instruction_message[i].append(Image(os.path.join(self.IMAGE_PATH, "instruction-4.png"), alpha=False))
            self.instruction_message[i].append(Image(os.path.join(self.IMAGE_PATH, "instruction-5.png"), alpha=False))
            
            self.instruction[i]["message"] = self.instruction_message[i][0]
            self.instruction[i]["message"].x = 40
            self.instruction[i]["message"].y = y_pos_icons + 60
        
        # 注：この画像は設定画面の一番下に表示されるものである。
        # この時点でiおよびy_pos_iconsの値は、最後のiの値になっていることに注意。
        self.instruction[i]["instruction_note"] = Image(os.path.join(self.IMAGE_PATH, "instruction-menu.png"), alpha=False)
        self.instruction[i]["instruction_note"].x = 40
        self.instruction[i]["instruction_note"].y = y_pos_icons + 120
        
        for i in range(4):
            for image in self.instruction[i].values():
                self.sprites.add(image)
        
        self.last_press_key = []
        for dummy in self.joypads:
            self.last_press_key.append({})
        # last_press_key: 各プレイヤーが、いつ最後にキーを押したか
        # - X: 整数
        # - Y: キーの名前（キーボードに対する名前を転用。K_RIGHTとかK_xとか）
        # * プレイヤーXがキーYを押した場合、
        #   last_press_key[X][Y] = time.time() とする。
        # * プレイヤーXがキーを離した場合、
        #   last_press_key[X].pop(Y) とする。
        # * プレイヤーXがキーYを押しているかは、
        #   Y in last_press_key[X] で調べられる。
    
    def update(self):
        # Joypadによるカーソル操作
        # 各Joypadについて動きをチェックする
        for joypad_id in range(len(self.joypads)):
            # 直近のキー操作から
            xaxis = self.joypads[joypad_id].get_axis(0)
            yaxis = self.joypads[joypad_id].get_axis(1)
            time_now = time.time()
            if xaxis > 0.9:
                if (K_RIGHT in self.last_press_key[joypad_id]) and (time_now - self.last_press_key[joypad_id][K_RIGHT] < self.KEY_REPEAT_TIME): continue
                self.last_press_key[joypad_id][K_RIGHT] = time_now
            elif xaxis < -0.9:
                if (K_LEFT in self.last_press_key[joypad_id]) and (time_now - self.last_press_key[joypad_id][K_LEFT] < self.KEY_REPEAT_TIME): continue
                self.last_press_key[joypad_id][K_LEFT] = time_now
            elif yaxis > 0.9:
                if (K_DOWN in self.last_press_key[joypad_id]) and (time_now - self.last_press_key[joypad_id][K_DOWN] < self.KEY_REPEAT_TIME): continue
                self.last_press_key[joypad_id][K_DOWN] = time_now
            elif yaxis < -0.9:
                if (K_UP in self.last_press_key[joypad_id]) and (time_now - self.last_press_key[joypad_id][K_UP] < self.KEY_REPEAT_TIME): continue
                self.last_press_key[joypad_id][K_UP] = time_now
            else:
                pass
        
        # キーボードによるカーソル操作
        if Key.is_press(K_RIGHT):
            pass
        elif Key.is_press(K_LEFT):
            pass
        elif Key.is_press(K_DOWN):
            pass
        elif Key.is_press(K_UP):
            pass
