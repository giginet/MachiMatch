# -*- coding: utf-8 -*-
#
#    Created on 2011/05/12
#    Created by giginet
#

import settings
from pywaz.sprite.number import Number
from pywaz.utils.timer import Timer

class GameTimer(Number):
    def __init__(self):
        self.timer = Timer(settings.FPS*settings.YEARS)
        super(GameTimer, self).__init__(u"../resources/image/main/navigation/timer.png", w=36, h=90)
        self.x, self.y = settings.TIMER_POSITON
        self.align = Number.TEXTALIGNCENTER
        self.n = int((self.timer.max-self.timer.now)/settings.FPS)
    def update(self):
        self.timer.tick()
        self.n = int((self.timer.max-self.timer.now)/settings.FPS)
    def play(self):
        self.timer.play()
    def is_over(self):
        return self.timer.is_over()
    def reset(self):
        self.timer.reset()
    @property
    def now(self):
        return self.n