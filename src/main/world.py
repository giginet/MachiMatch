# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#

import pygame
import settings
from ground import Ground, Territory, Dummy
from immigrantManager import ImmigrantManager
from player import Player


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
                    panel = self._generate_territory(x, y) # ゲーム参加人数によって領土を置くかどうか調査
                else:
                    panel = Ground(x, y)
                row.append(panel)
            self._map.append(row)
    def _generate_territory(self, x, y):
        u"""
            x, yの位置に設置されるTerritoryを返す
            プレイヤー人数によって配置が異なるのでその処理をココで行う
        """
        if self.player_count == 1:
            if 6 <= x <= 9:
                return Territory(x, y, self.players[0])
            else:
                return Ground(x, y)                
        elif self.player_count == 2:
            u"""
                2-5 Player 1
                10-13 Player 2
            """
            if 2 <= x <= 5:
                return Territory(x, y, self.players[0])
            elif 10 <= x <= 13:
                return Territory(x, y, self.players[1])
            else:
                return Ground(x, y)
        elif self.player_count == 3:
            u"""
                1~4 Player 1
                6-9 Player 2
                11-14 Player 3
            """
            if 1 <= x <= 4:
                return Territory(x, y, self.players[0])
            elif 6 <= x <= 9:
                return Territory(x, y, self.players[1])
            elif 11 <= x <= 14:
                return Territory(x, y, self.players[2])
            else:
                return Ground(x, y)
        elif self.player_count == 4:
            return Territory(x, y, self.players[int(x/4)])
        
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
        return pygame.rect.Rect(settings.ROOT_POSITION[1], settings.ROOT_POSITION[0]-settings.STAGE_HEIGHT*20, 
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
                if self.get_panel_on(player.point).can_attach_road():
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
    def get_winner(self):
        max = 0
        winner = self.players[0]
        for player in self.players:
            if max < player.city.population:
                winner = player
                max = player.city.population
        return winner