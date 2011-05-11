# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#

import pygame
import settings
from pywaz.core.game import Game
from ground import Ground, Territory, Dummy
from immigrantManager import ImmigrantManager
from player import Player
from pywaz.sprite import OrderedUpdates


class World(object):
    u"""マップを管理するクラス"""
    def __init__(self, *args, **kwargs):
        self.players = []
        self.player_count = 4
        self.player_positions = []
        self.i_manager = ImmigrantManager(self)
        for n in xrange(0,self.player_count):
            p = Player(n, self)
            self.players.append(p)
            self.player_positions.append(p.point)
        self._generate_stage()
    def _generate_stage(self):
        u"""ステージを生成する"""
        self._map = []
        for x in xrange(settings.STAGE_WIDTH):
            row = []
            for y in xrange(settings.STAGE_HEIGHT):
                if y < 4:
                    panel = Territory(x, y, self.players[0]) # 本来はゲームに参加しているプレイヤー数によっていろいろ処理を分岐させるけどあとで
                else:
                    panel = Ground(x, y)
                row.append(panel)
            self._map.append(row)
    def get_panel_on(self, point):
        u"""渡されたpointにあるパネルを取ってくる。領域外の場合はDummyパネルを返す"""
        x = point.x
        y = point.y
        if self.is_valid(point):
            return self._map[x][y]
        else:
            return Dummy(point.x, point.y)
    def draw(self):
        u"""マップを描画する"""
        for col in self._map:
            for panel in col:
                if panel.point in self.player_positions:
                    for player in self.players:
                        if player.point == panel.point:
                            player.current_road.draw()
                            break
                else:
                    panel.draw()
        map(lambda p: p.draw(), self.players)
        self.i_manager.draw()
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
        u"""渡された座標が領域内かどうかを判定する"""
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
        self.i_manager.update()
    def get_panel_from(self, panel, direction):
        u"""
            panelからdirectionの向きにあるパネルを取り出す
            direction　上から時計回りに0~3
        """
        point = panel.point.clone()
        if direction==0:
            point.y -=1
        elif direction==1:
            point.x +=1
        elif direction==2:
            point.y +=1
        elif direction==3:
            point.x -=1
        return self.get_panel_on(point)