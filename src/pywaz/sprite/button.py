# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
from animation import Animation, AnimationInfo
from ..device.mouse import Mouse
from ..mixer.sound import Sound

class Button(Animation):
    pressed = False
    hovered = False
    animation_enable = False
    hover_image = True
    press_image = True
    hover_sound = None
    press_sound = None
    
    def __init__(self, filepath, w, h, x=0, y=0):
        super(Button, self).__init__(filepath, AnimationInfo(0,0,1,w,h), x=x, y=y)
        image_height = self.image.get_size()[1]
        if int(image_height/h) == 1:
            self.hover_image = False
            self.press_image = False
        elif int(image_height/h) == 2:
            self.press_image = False
    
    def _on_mouseout(self):
        self.ainfo.index = 0
        self.on_mouseout()
    
    def _on_mouseover(self):
        if self.hover_image: self.ainfo.index = 1
        if self.hover_sound: Sound(self.hover_sound).play()
        self.on_mouseover()
    
    def _on_press(self):
        if self.press_image: self.ainfo.index = 2
        if self.press_sound: Sound(self.press_sound).play()
        self.on_press()
    
    def _on_release(self):
        self.on_release()
        
    def on_mouseout(self, *args, **kwargs):pass
    def on_mouseover(self, *args, **kwargs):pass
    def on_press(self, *args, **kwargs):pass
    def on_release(self, *args, **kwargs):pass
    
    def update(self):
        if self.hit_area.collidepoint(Mouse.get_pos()):
            if not self.hovered:
                self._on_mouseover()
            self.hovered = True
            if Mouse.is_press('LEFT'):
                if not self.pressed:
                    self._on_press()
                    self.pressed = True
            else:
                if self.pressed:
                    self._on_release()
                    self.pressed = False
        else:
            if self.hovered:
                self._on_mouseout()
            self.pressed = False
            self.hovered = False