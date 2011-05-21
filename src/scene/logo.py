# -*- coding: utf-8 -*-
#
#    Created on 2011/04/17
#    Created by giginet
#
import pygame

from pywaz.scene.abstractscene import Scene
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse
from pywaz.device.joypad import JoyPad

class LogoScene(Scene):
    BACKGROUND = (255,255,255)
    def ready(self, *args, **kwargs):
        super(LogoScene, self).ready()
        self.background = Image("../resources/image/menu/whiteback.png", alpha=False)
        self.logo = Image("../resources/image/menu/kawaz.png", alpha=False)
        self.logo.x = 340
        self.logo.y = 230
        self.sprites.add(self.background)
        self.sprites.add(self.logo)
        self.timer = Timer(210)
        self.mouse = Mouse(0)
        self.joypads = [] 
        for i in xrange(0, JoyPad.get_num_joypads()):
            self.joypads.append(JoyPad(i))        
    def update(self):
        self.timer.tick()
        self.timer.play()
        skip = self.mouse.is_press(Mouse.LEFT)
        for joypad in self.joypads:
            skip |= joypad.is_press(4)
        if self.timer.is_over() or skip:
            Game.get_scene_manager().change_scene('mainmenu')
        elif self.timer.now < 60:
            self.logo.alpha = 255*self.timer.now/60
        elif 120 < self.timer.now:
            self.logo.alpha = 255*(180-self.timer.now)/60