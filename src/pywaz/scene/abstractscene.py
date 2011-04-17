# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
from pywaz.sprite.image import Image
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game

class Scene(object):
    key = u"AbstractScene"
    BACKGROUND = (0,0,255)
    
    def __init__(self):
        self.sprites = OrderedUpdates()
    
    def ready(self, *args, **kwargs):
        Game.get_screen().fill(self.BACKGROUND)
    
    def update(self, *args, **kwargs):
        self.sprites.update(*args, **kwargs)
    
    def draw(self, surface=Game.get_screen()):
        update_rect = []
        update_rect += self.sprites.draw(surface)
        return update_rect
        
    def finalize(self):
        self.sprites.empty()