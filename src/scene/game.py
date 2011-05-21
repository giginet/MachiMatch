# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings
import pygame

from pywaz.sprite.image import Image
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.mixer.bgm import BGM
from pywaz.scene.manager import SceneManager
from pywaz.scene.abstractscene import Scene
from pywaz.utils.timer import Timer

from main.world import World
from main.navigation import Navigation
from main.gametimer import GameTimer

class GameScene(Scene):
    BACKGROUND = (153,255,255)
    def ready(self, *args, **kwargs):
        self.world = World(players=kwargs.get('players', 1))
        self.navigations = []
        self.timer = GameTimer()
        self.sequence_manager = SceneManager()
        self.sequence_manager.set_scenes({'ready':ReadySequence(self),
                                          'game':GameSequence(self),
                                          'result':ResultSequence(self),
                                          'pause':PauseSequence(self),
                                          })
        self.sequence_manager.change_scene('ready')
        for player in self.world.players:
            self.navigations.append(Navigation(player))
        self.timer.play()
    def update(self):
        self.sequence_manager.current_scene.update()
        super(GameScene, self).update()
    def draw(self):
        super(GameScene, self).draw()
        rect = self.sequence_manager.current_scene.draw()
        return rect
    
class Sequence(Scene):
    def __init__(self, scene, *args, **kwargs):
        self.scene = scene
        super(Sequence, self).__init__()
        self.text = Animation(u"../resources/image/main/text/game.png", AnimationInfo(-1, 0, 1, 360, 225, 1))
        self.text.animation_enable = False
        self.text.x = settings.SCREENWIDTH/2-180
        self.text.y = settings.SCREENHEIGHT/2-180
class ReadySequence(Sequence):
    def ready(self):
        self.ready_timer = Timer(settings.FPS*3)
        self.ready_timer.play()
    def update(self):
        self.ready_timer.tick()
        if self.ready_timer.now == settings.FPS*1:
            self.text.ainfo.index = 0
        elif self.ready_timer.now >= settings.FPS*2:
            self.text.ainfo.index = 1
            self.scene.sequence_manager.change_scene('game')
    def draw(self):
        rect = self.scene.world.draw()
        map(lambda n: n.draw(), self.scene.navigations)
        self.scene.timer.draw()
        self.text.draw()
        return rect
class GameSequence(Sequence):
    def ready(self):
        self.scene.timer.play()
        self.text.ainfo.index = 1
    def update(self):
        if self.text.y > -360:
            self.text.y -=30
        if self.scene.timer.is_over():
            self.scene.sequence_manager.change_scene('result')
        for player in self.scene.world.players:
            player.update()
            p = player.poll()
            u"""p=0のとき、何もしない、p=1のとき、右回転、p=2のとき設置、p=-1のとき左回転p=3のときポーズ"""
            if p == 3:
                self.scene.sequence_manager.change_scene('pause')
            elif p == 2:
                if self.scene.world.get_panel_on(player.point).can_attach_road():
                    self.scene.world.replace_panel(player.current_road)
                    player.attach_road()
            elif p!=0:
                player.current_road.rotate(p)
        self.scene.world.update()
        map(lambda n: n.update(), self.scene.navigations)
        self.scene.timer.update()
    def draw(self):
        rect = self.scene.world.draw()
        map(lambda n: n.draw(), self.scene.navigations)
        self.scene.timer.draw()
        if self.text.y > -360:
            self.text.draw()
        return rect
class ResultSequence(Sequence):
    def ready(self):
        self.win = Animation(u"../resources/image/main/text/win.png", AnimationInfo(-1, 0, 1, 360, 225, 1))
        self.win.animation_enable = False
        self.win.x = settings.SCREENWIDTH/2-180
        self.win.y = settings.SCREENHEIGHT/2-180
        self.text.ainfo.index = 3
        self.winner = self.scene.world.get_winner()
        self.result_timer = Timer(settings.FPS*2)
        self.result_timer.play()
    def update(self):
        self.result_timer.tick()
        if self.result_timer.now == settings.FPS*2:
            self.text.ainfo.index = -1
            self.win.ainfo.index = self.winner.number
        #ToDo Retry or Title
    def draw(self):
        rect = self.scene.world.draw()
        map(lambda n: n.draw(), self.scene.navigations)
        self.scene.timer.draw()
        self.text.draw()
        self.win.draw()
        return rect
class PauseSequence(Sequence):
    def ready(self):
        self.text.ainfo.index = 2
    def draw(self):
        rect = self.scene.world.draw()
        map(lambda n: n.draw(), self.scene.navigations)
        self.scene.timer.draw()
        self.text.draw()
        return rect
    def update(self):
        for player in self.scene.world.players:
            p = player.poll()
            u"""p=0のとき、何もしない、p=1のとき、右回転、p=2のとき設置、p=-1のとき左回転p=3のときポーズ"""
            if p == 3:
                self.scene.sequence_manager.change_scene('game')