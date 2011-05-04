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

from main.roads import LShapeRoad

class World(object):
    u"""マップを管理するクラス"""
    def __init__(self, *args, **kwargs):
        self._generate_stage()
        self.players = OrderedUpdates()
        self.player_count = 1
        for n in xrange(0,self.player_count):
            self.players.add(Player(0))
    def _generate_stage(self):
        u"""ステージを生成する"""
        self._map = []
        for x in xrange(settings.STAGE_WIDTH):
            row = []
            for y in xrange(settings.STAGE_HEIGHT):
                if y < 4:
                    panel = Territory(x, y, 1)
                else:
                    panel = Ground(x, y)
                row.append(panel)
            self._map.append(row)
    def get_panel_on(self, point):
        x = point.x
        y = point.y
        return self._map[x][y]
    def draw(self):
        u"""マップを描画する"""
        for col in self._map:
            for panel in col:
                for player in self.players:
                    if panel.point == player.point:
                        player.current_road.alpha = 0.5
                        player.current_road.draw()
                        break
                    else:
                        panel.draw()
        self.players.draw(Game.get_screen())
        return pygame.rect.Rect(settings.ROOTY, settings.ROOTX-settings.STAGE_HEIGHT*20, 
                                settings.STAGE_HEIGHT*20, settings.STAGE_WIDTH*20)
    def _replace_panel(self, panel):
        u"""Map上のパネルを置き換える"""
        x = panel.point.x
        y = panel.point.y
        outdated_panel = self._map[x][y]
        self._map[x][y] = panel
        del outdated_panel
    def is_valid(self, point):
        x = point.x
        y = point.y
        return 0 <= x < settings.STAGE_WIDTH and 0 <= y < settings.STAGE_HEIGHT
    def update(self):
        for col in self._map:
            for panel in col:
                if panel.is_road() and panel.update() == 1:
                    ground = Ground(panel.point.x, panel.point.y)
                    self._replace_panel(ground)
        for player in self.players:
            player.update()
            p = player.poll()
            u"""p=0のとき、何もしない、p=1のとき、右回転、p=2のとき設置、p=-1のとき左回転"""
            if p == 2:
                self._replace_panel(player.current_road)
                player.attach_road()
            elif p!=0:
                player.current_road.rotate(p)