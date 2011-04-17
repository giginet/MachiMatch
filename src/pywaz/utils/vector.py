# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import math

def require_vector(func):
    u"""引数がベクトルであることを要求するデコレータ"""
    def decorated(*args):
        if not isinstance(args[1], Vector): raise TypeError
        return func(*args)
    return decorated

class Vector(object):
    u"""2Dベクトルを扱うクラス"""
    def __init__(self, *args):
        if isinstance(args[0], tuple): 
            self.set(args[0][0], args[0][1])
        else: 
            self.set(args[0], args[1])
    def __str__(self):
        return "(%f, %f)" % (self.x, self.y)
    def __unicode__(self):
        return u"(%f, %f)" % (self.x, self.y)
    @require_vector
    def __lt__(self, v): return self.length < v.length
    @require_vector
    def __lte__(self, v): return self.length <= v.length
    @require_vector
    def __eq__(self, v): return self.x == v.x and self.y == v.y
    @require_vector
    def __gte__(self, v): return self.length >= v.length
    @require_vector
    def __gt__(self, v): return self.length > v.length
    
    @require_vector        
    def add(self, v):
        self.x += v.x
        self.y += v.y
        return self 
    def __add__(self, v): 
        x = self.x + v.x
        y = self.y + v.y
        return Vector(x,y)
        
    @require_vector
    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        return self
    def __sub__(self, v): 
        x = self.x - v.x
        y = self.y - v.y
        return Vector(x,y)
    
    def mul(self, v):
        import numbers
        if isinstance(v, Vector):
            return self.scalar_product(v)
        elif isinstance(v, numbers.Number):
            return self.scale(v)
        raise TypeError
    def __mul__(self, *args): 
        import numbers
        if isinstance(args[0], Vector):
            return self.scalar_product(args[0])
        elif isinstance(args[0], numbers.Number):
            x = self.x*args[0]
            y = self.y*args[0]
            return Vector(x,y)
        raise TypeError
    
    def div(self, n):
        self.x /= n
        self.y /= n
        return self
    def __div__(self, n): 
        x = self.x/n
        y = self.y/n
        return Vector(x,y)
    
    def scale(self, n):
        u"""ベクトルをスカラ倍する"""
        self.x *= n
        self.y *= n
        return self
    
    @require_vector    
    def scalar_product(self, v):
        u"""ベクトルの外積を取る（そのうち3次元に拡張）"""
        return Vector(0,0)
    
    def set(self, x, y):
        u"""ベクトルに指定の値をセットする"""
        self.x = x
        self.y = y
    
    @property
    def length(self):
        return math.hypot(self.x, self.y)
    
    def normalize(self):
        u"""ベクトルを正規化する（長さを１にする）"""
        if self.length==0:
            return Vector(0, 0)
        else:
            return self.scale(1/self.length)
        
    def resize(self, size):
        u"""ベクトルを指定した長さにする"""
        return self.normalize().scale(size)
    
    @property
    def angle(self):
        u"""ベクトルの角度を返す"""
        return math.degrees(math.atan2(self.y, self.x))
    
    def rotate(self, deg):
        u"""ベクトルを回転させる"""
        rad = math.radians(deg)
        x = self.x
        y = self.y
        self.x = math.sin(rad)*y+math.cos(rad)*x 
        self.y = math.cos(rad)*y-math.sin(rad)*x
        return self
            
    def clone(self):
        u"""ベクトルをコピーする"""
        return Vector(self.x, self.y)
    
    def reverse(self):
        u"""逆ベクトルを返す"""
        self.x *= -1
        self.y *= -1
        return self
    
    def max(self, m):
        u"""ベクトルの最大長さを指定"""
        if self.length > m:
            self.resize(m)
        return self
    
    def min(self, m):
        u"""ベクトルの最小長さを指定"""
        if self.length < m:
            self.resize(m)
        return self
    
    def to_pos(self):
        return (self.x, self.y)
    
    def divide(self, length):
        u"""ベクトルを指定された長さ分に分割してリストで返す"""
        times = int(self.length/length)
        mod = self.length-length*times
        vs = []
        for i in xrange(times):
            vs.append(self.clone().resize(length))
        vs.append(self.clone().resize(mod))
        return vs