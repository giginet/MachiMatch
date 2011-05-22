# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings
import pygame

from pywaz.mixer.sound import Sound
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
        self.num_players = kwargs.get('players', 1)
        self.timer = GameTimer()
        self.sequence_manager = SceneManager()
        self.sequence_manager.set_scenes({'ready':ReadySequence(self),
                                          'game':GameSequence(self),
                                          'result':ResultSequence(self),
                                          'pause':PauseSequence(self),
                                          })
        self.bgm = BGM(u"../resources/music/main_intro.wav", -1, u"../resources/music/main_loop.wav")
        self.sequence_manager.change_scene('ready')
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
        self.scene.world = World(players=self.scene.num_players)
        self.scene.navigations = []
        for player in self.scene.world.players:
            self.scene.navigations.append(Navigation(player))
        self.text.ainfo.index = 0
        self.scene.bgm.set_volume(0.7)
        self.scene.timer.reset()
        self.scene.timer.update()
        self.ready_timer = Timer(settings.FPS*3)
        self.ready_timer.play()
    def update(self):
        self.scene.bgm.play()
        self.ready_timer.tick()
        if self.ready_timer.now == settings.FPS*1:
            self.text.ainfo.index = 0
        elif self.ready_timer.now >= settings.FPS*2:
            self.text.ainfo.index = 1
            self.scene.sequence_manager.change_scene('game')
            self.scene.sequence_manager.current_scene.text.x = settings.SCREENWIDTH/2-180
            self.scene.sequence_manager.current_scene.text.y = settings.SCREENHEIGHT/2-180
        
    def draw(self):
        rect = self.scene.world.draw()
        map(lambda n: n.draw(), self.scene.navigations)
        self.scene.timer.draw()
        self.text.draw()
        return rect
class GameSequence(Sequence):
    def ready(self):
        self.text.ainfo.index = 1
        self.scene.bgm.set_volume(1)
        self.rotate_sound = Sound(u"../resources/sound/rotate.wav")
        self.attach_sound = Sound(u"../resources/sound/attach.wav")
        self.pause_sound = Sound(u"../resources/sound/pause.wav")
    def update(self):
        self.scene.bgm.play()
        if self.text.y > -360:
            self.text.y -=30
        if self.scene.timer.is_over():
            self.scene.sequence_manager.change_scene('result')
        for player in self.scene.world.players:
            player.update()
            p = player.poll()
            u"""p=0のとき、何もしない、p=1のとき、右回転、p=2のとき設置、p=-1のとき左回転p=3のときポーズ"""
            if p == 3:
                self.pause_sound.play()
                self.scene.sequence_manager.change_scene('pause')
            elif p == 2:
                if self.scene.world.get_panel_on(player.point).can_attach_road():
                    self.scene.world.replace_panel(player.current_road)
                    self.attach_sound.play()
                    player.attach_road()
            elif p!=0:
                self.rotate_sound.play()
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
        finish_sound = Sound("../resources/sound/finish.wav")
        finish_sound.play()
        self.win.animation_enable = False
        self.win.x = settings.SCREENWIDTH/2-180
        self.win.y = settings.SCREENHEIGHT/2-180
        self.text.ainfo.index = 3
        self.winner = self.scene.world.get_winner()
        self.result_timer = Timer(settings.FPS*2.5)
        self.result_timer.play()
    def update(self):
        self.result_timer.tick()
        if self.result_timer.now == settings.FPS*2.5:
            self.text.ainfo.index = -1
            self.scene.bgm.fadeout(100)
            self.win.ainfo.index = self.winner.number
        for player in self.scene.world.players:
            p = player.poll()
            u"""p=3のとき、リプレイ"""
            if self.result_timer.is_over() and p == 3:
                self.scene.bgm.change(u"../resources/music/main_intro.wav", -1, u"../resources/music/main_loop.wav")
                self.scene.sequence_manager.change_scene('ready')
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
        self.scene.bgm.set_volume(0.4)
    def draw(self):
        rect = self.scene.world.draw()
        map(lambda n: n.draw(), self.scene.navigations)
        self.scene.timer.draw()
        self.text.draw()
        return rect
    def update(self):
        self.scene.bgm.play()
        for player in self.scene.world.players:
            p = player.poll()
            u"""p=0のとき、何もしない、p=1のとき、右回転、p=2のとき設置、p=-1のとき左回転p=3のときポーズ"""
            if p == 3:
                self.scene.sequence_manager.change_scene('game')