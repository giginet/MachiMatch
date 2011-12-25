# -*- coding: utf-8 -*-
#
#    Created on 2011/05/09
#    Created by giginet
#
import settings
import random
from pywaz.utils.timer import Timer
from pywaz.utils.vector import Vector
from pywaz.mixer.sound import Sound
from main.building import *
class City(object):
    u"""街クラス。人口や発展状況などを管理する"""    
    def __init__(self, owner, world):
        u"""
            owner : この街を所持するプレイヤー
            world : Worldクラスインスタンス
        """
        self.owner = owner
        self.world = world
        self.levelup_sound = Sound("../resources/sound/levelup.wav")
        self.increase_sound = Sound("../resources/sound/increase.wav")
        self.population = 0
        self.level = 1
        self.buildings = []
        self.territories = []
        self.flow_timer = Timer(settings.FPS*settings.FLOW_POPULATION_YEAR)
        self.building_matrix = [[None for col in range(settings.STAGE_HEIGHT)] for row in range(settings.STAGE_WIDTH)] # 二次配列を生成してNoneで初期化
        #self._constract_building(Laputa, 0, 0)
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
            self.levelup_sound.play()
            self.level +=1
        else:
            self.increase_sound.play()
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
    def _pop_building(self):
        u"""ビルを建てる"""
        if self.population <= 0: return
        if random.randint(0, settings.BUILDING_POP_RATE) != 0: return
        buildings = LEVEL_BUILDINGS[self.level-1]
        if len(buildings) == 0: return
        if self.level <= 2:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        elif self.level <= 4:
            x, y = random.choice(((0, 0), (2, 0), (0, 2), (2, 2)))
        elif self.level == 5:
            x, y = (0, 0)
        if not self.building_matrix[x][y] or (self.building_matrix[x][y] and self.building_matrix[x][y].level != self.level):
                building = random.choice(buildings)
                self._constract_building(building, x, y)
    def _constract_building(self, cls, x, y):
        building = cls(self.root_point.x+x, self.root_point.y+y)
        for sx in xrange(x, x+building.size):
            for sy in xrange(y, y+building.size):
                self.building_matrix[sx][sy] = building
        self.buildings.append(building)
    
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
        self._pop_building()
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
        u"""移民を流出させる"""
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
        u"""街の左上の座標を返す"""
        pc = self.world.player_count
        if pc == 1:
            return Vector(6, 0)
        elif pc == 2:
            return (Vector(2, 0), Vector(10, 0))[self.owner.number]
        elif pc == 3:
            return (Vector(1, 0), Vector(6, 0), Vector(11, 0))[self.owner.number]
        elif pc == 4:
            return Vector(self.owner.number*4, 0)
