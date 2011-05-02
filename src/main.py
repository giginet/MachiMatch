# -*- coding: utf-8 -*-
#
#    Created on 2011/05/03
#    Created by giginet
#
import pygame
from pygame.locals import *

import settings

from pywaz.core.game import Game
from pywaz.scene.abstractscene import Scene
from pywaz.device.key import Key

from scene.logo import *
from scene.game import *

def main():
    pygame.mixer.pre_init(44100, -16, 2, 1024*3)
    pygame.init() # pygameの初期化
    
    game = Game()
    game.get_scene_manager().set_scenes({'logo':LogoScene(), 'game':GameScene(), })
    if settings.DEBUG:        
        game.get_scene_manager().change_scene('game')
    else:
        game.get_scene_manager().change_scene('logo')
    while 1:
        game._clock.tick(settings.FPS)
        Key.poll()
        scene = game.current_scene()
        if not scene: return
        game.update()
        rects = game.draw()
        pygame.display.update(rects) # 画面を反映
        for event in pygame.event.get(): # イベントチェック
            if event.type == QUIT: return
            if (event.type == KEYDOWN and event.key  == K_ESCAPE): return
if __name__ == '__main__': main()