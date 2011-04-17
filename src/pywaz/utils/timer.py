# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
class Timer(object):
    u"""フレーム管理を行うクラス"""
    def __init__(self, m=0,loop=False):
        self.init(m)
        self.enable_loop = loop

    def init(self, m=0):
        self._time = 0
        self.set(m)
        self._f_active = False
        self.enable_loop = False
        
    def set(self, m):
        self._max = m
    
    @property
    def max(self):
        return self._max
    
    @property
    def now(self):
        return self._time
    
    def tick(self):
        self.count()
        if self.is_over():
            if self.enable_loop:
                self.reset()
                
    def play(self):
        self._f_active = True
        return self
        
    def stop(self):
        self._time = 0
        self._f_active = False
        return self
        
    def pause(self):
        self._f_active = False
        return self
    
    def reset(self):
        self._time = 0
        return self
    
    def count(self):
        if self._f_active and self._time < self._max:
            self._time +=1
            
    def is_active(self):
        return self._f_active
    
    def is_over(self):
        return self._time >= self._max

    def move(self, n):
        self._time += n
        if self.is_over():
            if self.enable_loop:
                self._time = self._time % self._max
                
    def kill(self):
        pass