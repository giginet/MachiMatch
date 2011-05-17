# -*- coding: utf-8 -*-
#
#    Created on 2011/05/09
#    Created by giginet
#
import settings
import random
from pywaz.utils.timer import Timer
from pywaz.utils.vector import Vector
from main.building import *;
class City(object):
    u"""街クラス。人口や発展状況などを管理する"""
    def __init__(self, owner, world):
        u"""
            owner : この街を所持するプレイヤー
            world : Worldクラスインスタンス
        """
        self.owner = owner
        self.world = world
        self.population = 0
        self.level = 1
        self.buildings = []
        self.territories = []
        self.flow_timer = Timer(settings.FPS*settings.FLOW_POPULATION_YEAR)
        self.building_matrix = []
        for x in xrange(0, 4):
            row = []
            for y in xrange(0, 4):
                u"""領土内相対座標の二次配列作成"""
                row.append(None)
            self.building_matrix.append(row)
    def increase_population(self, p=None):
        u"""人口を増やす。その後、レベルアップの判定をする
            増える人口はレベルに依存する。 p*2^(lv-1)
        """
        self.flow_timer.reset()
        self.flow_timer.play()
        if not p:
            self.population += self._calc_population()
        else:
            self.population += p
        if self.level < 5 and settings.LEVELUP_BORDERLINES[self.level] < self.population:
            self.level +=1
            print "LevelUp! %d" % self.level
    def decrease_population(self, p):
        u"""
            p人人口を減らす
            実際に減った人数を返す
        """
        self.flow_timer.reset()
        self.flow_timer.play()
        if self.population < p:
            p = self.population
            self.population = 0
        else:
            self.population -= p
        return p
    def _create_building(self):
        if self.population <= 0: return
        if random.randint(0, settings.BUILDING_POP_RATE) != 0: return
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        if not self.building_matrix[x][y] or (self.building_matrix[x][y] and self.building_matrix[x][y].level != self.level):
            bs = LEVEL_BUILDINGS[self.level-1]
            if len(bs) == 0: return
            building = random.choice(bs)(self.root_point.x+x, self.root_point.y+y)
            for sx in xrange(x, x+building.size):
                for sy in xrange(y, y+building.size):
                    self.building_matrix[sx][sy] = building
    def _calc_population(self):
        u"""レベルに応じた増減する人口を算出する"""
        p = random.randint(8000, 12000)
        return p*2**(self.level-1)
        
    def update(self):
        self.flow_timer.tick()
        if self.flow_timer.is_over() and self.population > 0:
            u"""人を流出させる"""
            bottom_territories = self._get_bottom_territories()
            for territory in bottom_territories:
                u"""最も手前にある領土の一覧を取ってきて、繋がっているかどうか調査する"""
                front = self.world.get_panel_from(territory, 2)
                if territory.is_connect_with(front):
                    self._flow_immigration(territory, front)
        self._create_building()
        updated = []
        for x in xrange(0, 4):
            for y in xrange(0, 4):
                b = self.building_matrix[x][y]
                if b and not b in updated:
                    b.update()
                    updated.append(b)
    def draw(self):
        rendered = []
        for x in xrange(0, 4):
            for y in xrange(0, 4):
                b = self.building_matrix[x][y]
                if b and not b in rendered:
                    b.draw()
                    rendered.append(b)
    def _flow_immigration(self, territory, front):
        immigrant = self.world.i_manager.create_immigrant(territory.point.x, territory.point.y)
        p = self._calc_population()
        p = self.decrease_population(p)
        immigrant.population = p
        immigrant.direction = 2
        immigrant.ainfo.index = 2
        immigrant.current_ground = territory
        immigrant.x, immigrant.y = territory.surface_bottom_edge.to_pos()
        immigrant.goal_ground = front
        self.flow_timer.reset()
    def _get_bottom_territories(self):
        u"""領土最下層のTerritoryのみを取ってくる"""
        list = []
        for territory in self.territories:
            if territory.point.y == 3:
                list.append(territory)
        return list
    @property
    def root_point(self):
        return Vector(self.owner.number*4, 0)