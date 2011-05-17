# -*- coding: utf-8 -*-
#
#    Created on 2011/04/17
#    Created by giginet
#
import pygame

from pywaz.scene.abstractscene import Scene
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.mixer.bgm import BGM
from pywaz.utils.vector import Vector
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse
from pywaz.sprite.button import Button

class LogoScene(Scene):
    BACKGROUND = (255,255,255)
    def ready(self, *args, **kwargs):
        super(LogoScene, self).ready()
        self.background = Image("../resources/image/menu/whiteback.png", alpha=False)
        self.logo = Image("../resources/image/menu/kawaz.png", alpha=False)
        self.logo.x = 273
        self.logo.y = 260
        self.sprites.add(self.background)
        self.sprites.add(self.logo)
        self.timer = Timer(210)
        
    def update(self):
        self.timer.tick()
        self.timer.play()
        if self.timer.is_over() or Mouse.is_press('LEFT'):
            Game.get_scene_manager().change_scene('mainmenu')
        elif self.timer.now < 60:
            self.logo.alpha = 255*self.timer.now/60
        elif 120 < self.timer.now:
            self.logo.alpha = 255*(180-self.timer.now)/60