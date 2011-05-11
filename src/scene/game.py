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
from main.navigation import Navigation

class GameScene(Scene):
    BACKGROUND = (153,255,255)
    def ready(self, *args, **kwargs):
        self.world = World()
        self.navigations = []
        for player in self.world.players:
            self.navigations.append(Navigation(player))
    def update(self):
        self.world.update()
        map(lambda n: n.update(), self.navigations)
        super(GameScene, self).update()
    def draw(self):
        super(GameScene, self).draw()
        rect = self.world.draw()
        map(lambda n: n.draw(), self.navigations)
        return rect