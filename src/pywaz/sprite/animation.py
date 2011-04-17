# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame

from ..sprite.image import Image
from ..core.game import Game
from ..utils.timer import Timer
from ..utils.vector import Vector

class AnimationInfo(object):
    u"""Animation Info"""
    def __init__(self, index, frame, max_frame, width, height, apf = 10, loop=True):
        u"""Constructor of AnimationInfo

        Attribute:
            index       - index of animation (Y)
            frame       - frame of animation (X)
            max_frame   - the number of frame of Animation
            width       - the frame width
            height      - the frame height
            apf         - animation per frame
            loop        - flag for looping animation
        """
        self.index = index
        self.frame = frame
        self.max_frame = max_frame
        self.width = width
        self.height = height
        self.apf = apf
        self.loop = loop
    def next_frame(self):
        u"""Increase current frame number"""
        if self.frame < self.max_frame:
            self.frame += 1
        if self.loop:
            self.frame = 0 if self.frame >= self.max_frame else self.frame
        return self.frame
    def previous_frame(self):
        u"""Decrease current frame number"""
        if self.frame >= 0:
            self.frame -= 1
        if self.loop:
            self.frame = self.max_frame-1 if self.frame < 0 else self.frame
        return self.frame
    
class Animation(Image):
    u"""Sprite with Animation"""
    animation_enable = True
    animation_reverse = False

    def __init__(self, path, ainfo, x=0, y=0):
        u"""Constructor of AnimationSprite

        Attribute:
            image       - image path of this sprite
            ainfo       - animation info of this sprite
        """
        super(Animation, self).__init__(path, None,x=x,y=y)
        self.ainfo = ainfo
        self.center = Vector(self.ainfo.frame*self.ainfo.width, self.ainfo.index*self.ainfo.height)+Vector(self.ainfo.width, self.ainfo.height)*0.5
        self.rect = pygame.Rect(0, 0, self.ainfo.width, self.ainfo.height)
        self.hit = pygame.Rect(0, 0, self.ainfo.width, self.ainfo.height)
        self.animation_wait = Timer(ainfo.apf) 
        self.animation_wait.play()
        
        self.on_animation_over = None
        self.on_frame_change = None
    
    @property
    def draw_area(self):
        u"""area info automatically generate from `ainfo`"""
        # Notice: The algorithms below is fit only for single line animation file
        w = self.ainfo.width
        h = self.ainfo.height
        x = self.ainfo.frame * w
        y = self.ainfo.index * h
        return pygame.Rect(x, y, w, h)
    
    def update(self):
        super(Animation, self).update()
        if self.animation_enable:
            self.animation_wait.tick()
            if self.animation_wait.is_over():
                if not self.animation_reverse:
                    frame = self.ainfo.next_frame()
                else:
                    frame = self.ainfo.previous_frame()
                if self.on_frame_change: self.on_frame_change(self)
                if frame == 0:
                    if self.on_animation_over: self.on_animation_over(self)
                self.animation_wait.reset().play()
        
    
    def draw(self, surface=Game.get_screen(), dest=None, special_flags = 0):
        u"""Draw this sprite to the surface and animate

        Attribute:
            surface     - the target surface
            dest        - the `Rect` of where to draw on the surface
        """
        updated_rect = super(Animation, self).draw(surface, dest, self.draw_area, special_flags)
        return updated_rect
    
    def is_over(self):
        return self.ainfo.frame == self.ainfo.max_frame - 1
    
    def _rotate(self, image, dest, center=None):
        return self.image, dest
    def _resize(self, image, dest):
        return self.image, dest