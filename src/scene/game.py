# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings
import pygame

from pywaz.sprite.image import Image
from pywaz.mixer.bgm import BGM
from pywaz.scene.manager import SceneManager
from pywaz.scene.abstractscene import Scene

from main.world import World

class GameScene(Scene):
    BACKGROUND = (153,255,255)
    def ready(self, *args, **kwargs):
        self.world = World()
    def update(self):
        self.world.update()
        super(GameScene, self).update()
    def draw(self):
        super(GameScene, self).draw()
        rect = self.world.draw()
        return rect
        