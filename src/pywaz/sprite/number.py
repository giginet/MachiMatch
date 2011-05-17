# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#


import pygame

from pygame.rect import Rect
from pygame.sprite import Sprite
from pywaz.sprite.image import Image
from pywaz.core.game import Game

class Number(Sprite):
    u"""
        表示する数値を変更する : NumberInstance.n = 100
        文字のそろえを変更する : NumberInstance.align = Number.TEXTALIGNLEFT or Number.TEXTALIGNRIGHT or Number.TEXTALIGNCENTER
    """
    TEXTALIGNLEFT = 0
    TEXTALIGNRIGHT = 1
    TEXTALIGNCENTER = 2
    def __init__(self, filepath, n=0, x=0, y=0, w=20, h=40, margin=0):
        u"""
            filepath : 文字スプライトの画像パス(0-9まで等幅で並んでいる必要がある)
            n        : 初期表示数字
            x,y      : 表示位置座標
            w        : 数字一つの幅
            h        : 画像の高さ
            margin   : 桁同士の隙間
        """
        super(Number, self).__init__()
        self.width = w
        self.height = h
        self.margin = margin
        self.n = int(n)
        self.align = self.TEXTALIGNLEFT # 左揃えor右揃え
        self.pre_n = self.n
        self.x = x
        self.y = y
        self.filepath = filepath
        self._parse()
        
    def _parse(self):
        if self.n < 0:
            self.n = 0
        place = len(str(self.n)) # 桁
        self.image = pygame.surface.Surface((self.width*place+self.margin*place, self.height))
        self.image.set_colorkey((0,0,0))
        dest = self.image.get_rect().move(self.x, self.y)
        area = dest
        for i,s in enumerate(str(self.n)):
            n = int(s)
            image = Image(self.filepath)
            dest = pygame.rect.Rect((self.width+self.margin)*i,0, self.width, self.height)
            area = Rect(n*self.width, 0, self.width, self.height)
            self.image.blit(image.image, dest, area)
    
    def draw(self, surface=Game.get_screen()):
        if self.n != self.pre_n:
            self.pre_n = self.n
            self._parse()
        dest = self.image.get_rect().move(self.x, self.y)
        if self.align == self.TEXTALIGNRIGHT:
            u"""右揃えに変更する"""
            dest = dest.move(-self.image.get_width(), 0)
        elif self.align == self.TEXTALIGNCENTER:
            u"""中央揃えに変更する"""
            dest = dest.move(-self.image.get_width()/2, 0)
        return surface.blit(self.image, dest=dest)
    
    def get_surface(self):
        return self.image