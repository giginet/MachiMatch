# -*- coding: utf-8 -*-
#
#    Created on 2011/02/12
#    Created by giginet
#
#    refer to http://www.halb-katze.jp/pygt/src/music/music.py
import pygame

from pygame.mixer import music
from pywaz.utils.singleton import Singleton

class BGM(Singleton):
    def __init__(self, filename, loop=0, loopfile=None):
        self._set(filename, loop, loopfile)
        self._reset()

    def _load_file(self, filename):
        try:
            music.load(filename)
        except pygame.error, message:
            print u"""'%s' is not exist.""" % filename
            raise IOError, message

    def _set(self, filename, loop=0, loopfile=None):
        self.loop = loop
        self.introfile = filename
        self.loopfile = loopfile
        self._load_file(filename)

    def change(self, filename, loop=0, loopfile=None, ms=500):
        self.fadeout(ms)
        self._set(filename, loop, loopfile)
        self._reset()

    def _reset(self):
        self.intro = True
        self.looping = False
        self.stop = False

    def play(self):
        u"""音楽を再生する。ループに放り込んで使う"""
        if not self.stop:
            if not self.loopfile:
                if not self.looping and not music.get_busy():
                    music.play(self.loop)
                    self.looping = True
            else: # イントロとループに分かれてる場合
                if self.intro: # イントロ再生要求時
                    if not music.get_busy():
                        music.play()
                    self.intro = False
                else:
                    if not self.looping:
                        if not music.get_busy():
                            music.load(self.loopfile)
                            music.play(-1)
                            self.looping = True

    def fadeout(self, msec):
        music.fadeout(msec)
        self.stop = True
    
    @staticmethod
    def set_volume(volume):
        music.set_volume(volume)