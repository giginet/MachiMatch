# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame

class Window(object):
    def __init__(self, width=640, height=480, caption=u"Hello, World"):
        self.window = pygame.display.set_mode( (width, height) ) # 画面を作る
        pygame.display.set_caption(caption) # タイトル
        pygame.display.flip() # 画面を反映
        
    def blit(self, image, imagerect):
        self.window.blit(image, imagerect)
        
    def fill(self, tuple):
        self.window.fill(tuple)