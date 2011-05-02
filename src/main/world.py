# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#

import pygame
import settings
from pywaz.core.game import Game
from ground import Ground, Territory
from player import Player
from pywaz.sprite import OrderedUpdates

class World(object):
    u"""マップを管理するクラス"""
    def __init__(self, *args, **kwargs):
        self._generate_stage()
        self.players = OrderedUpdates()
        for n in xrange(0,1):
            self.players.add(Player(0))
    def _generate_stage(self):
        u"""ステージを生成する"""
        self._map = []
        self.panels = OrderedUpdates()
        for y in xrange(settings.STAGE_HEIGHT):
            column = []
            for x in xrange(settings.STAGE_WIDTH):
                if y < 4:
                    panel = Territory(x, y, 1)
                else:
                    panel = Ground(x, y)
                column.append(panel)
                self.panels.add(panel)
            self._map.append(column)
    def draw(self):
        u"""マップを描画する"""
        self.panels.draw(Game.get_screen())
        self.players.draw(Game.get_screen())
        return pygame.rect.Rect(settings.ROOTY, settings.ROOTX-settings.STAGE_HEIGHT*20, 
                                settings.STAGE_HEIGHT*20, settings.STAGE_WIDTH*20)
    def update(self):
        for player in self.players:
            player.update()