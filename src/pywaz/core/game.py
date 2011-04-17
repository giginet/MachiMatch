# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
import settings
from pygame.locals import *

from ..utils.singleton import Singleton
from window import Window
from ..scene.manager import SceneManager
from ..device.key import Key

class Game(Singleton):
    _clock = pygame.time.Clock()
    _scene_manager = SceneManager()
    _screen = Window(width=settings.SCREENWIDTH, height=settings.SCREENHEIGHT, caption=settings.SCREENCAPTION)
        
    @classmethod
    def get_screen(cls):
        return cls._screen.window
    
    @classmethod
    def update(cls):
        cls._scene_manager.update()
        
    @classmethod
    def draw(cls):
        return cls._scene_manager.draw()
        
    @classmethod
    def get_scene_manager(cls):
        return cls._scene_manager
    
    @classmethod
    def current_scene(cls):
        return cls._scene_manager.current_scene
    
    @classmethod
    def set_caption(cls, caption):
        pygame.display.set_caption(caption)
    
    @classmethod
    def add(cls, sprite):
        cls.current_scene().sprites.add(sprite)
    
    @classmethod
    def mainloop(cls):
        while 1:
            cls._clock.tick(60)
            cls._screen.fill(cls.current_scene().BACKGROUND) # 画面のクリア
            Key.poll()
            cls.update()
            cls.draw()
            pygame.display.flip() # 画面を反映
            for event in pygame.event.get(): # イベントチェック
                if event.type == QUIT: # 終了が押された？
                    return
                if (event.type == KEYDOWN and
                    event.key  == K_ESCAPE): # ESCが押された？
                    return