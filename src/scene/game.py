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


class GameScene(Scene):
    def ready(self, *args, **kwargs):
        pass
    def update(self):
        super(GameScene, self).update()
        pass
    def draw(self):
        return super(GameScene, self).draw()
        