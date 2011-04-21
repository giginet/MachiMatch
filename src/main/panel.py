# -*- coding: utf-8 -*-
#
#    Created on 2011/04/20
#    Created by giginet
#

from pywaz.sprite.image import Image
from pywaz.utils.vector import Vector

class Panel(Image):
    NODE = 0
    IMAGEPATH = u"../resources/image/main/chips/chipM.png"
    def __init__(self, x, y):
        self.point = Vector(x, y)
        #道がつながっているかどうかを2進数表記で保持する
        #上右下左=1111
        self.node = int(str(self.NODE), 2)
        super(Panel, self).__init__(self.IMAGEPATH)
    @property
    def up(self):
        return self.node & 8
    @property
    def right(self):
        return self.node & 4
    @property
    def down(self):
        return self.node & 2
    @property
    def left(self):
        return self.node & 1 
    