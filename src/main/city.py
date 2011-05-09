# -*- coding: utf-8 -*-
#
#    Created on 2011/05/09
#    Created by giginet
#
class City(object):
    u"""街クラス。人口や発展状況などを管理する"""
    def __init__(self, owner, world):
        u"""
            owner : この街を所持するプレイヤー番号。0~3
            world : Worldクラスインスタンス
        """
        self.owner = owner
        self.world = world
        self.population = 0
        self.level = 1
        self.buildings = []
        self.territories = []
    def increase_population(self, p):
        u"""人口を増やす。その後、レベルアップの判定をする
            増える人口はレベルに依存する。 p*2^(lv-1)
        """
        self.population += p*2**(self.level-1)
        print u"Player:%d %d人" % (self.owner+1, self.population)
        #ToDo LvUP判定