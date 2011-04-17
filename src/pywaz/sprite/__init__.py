import pygame
from pygame.sprite import Sprite

class _Mixin(object):
    def draw(self, surface):
        for sprite in self.sprites():
            if isinstance(sprite, Sprite):
                sprite.draw(surface)
            else:
                surface.blit(sprite.image, sprite.rect)
class _Mixin2(object):
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in self.sprites():
            r = spritedict[s]
            if isinstance(s, Sprite):
                newrect = s.draw(surface)
            else:
                newrect = surface_blit(s.image, s.rect)
            if r is 0:
                dirty_append(newrect)
            else:
                if newrect and newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                elif newrect:
                    dirty_append(newrect)
                    dirty_append(r)
            spritedict[s] = newrect
        return dirty
# group -----------------------------------------------------------------------------------
#
# Notice:
#   The order of inheritation is IMPORTANT
#
class Group(_Mixin, pygame.sprite.Group):
    pass
class RenderUpdates(_Mixin2, pygame.sprite.RenderUpdates):
    pass
class OrderedUpdates(_Mixin2, pygame.sprite.OrderedUpdates):
    pass
class LayeredUpdates(_Mixin2, pygame.sprite.LayeredUpdates):
    pass
# collide ---------------------------------------------------------------------------------
#
# Notice:
#   Only `collide_rect` and `spritecollide` is modified
#
from pygame.sprite import collide_rect_ratio
from pygame.sprite import collide_circle, collide_circle_ratio
from pygame.sprite import collide_mask
from pygame.sprite import groupcollide, spritecollideany

def collide_rect(left, right):
    u"""collision detection between two sprites, using `colrect` of each sprite"""
    return left.coltest_rect.colliderect(right.coltest_rect)

def spritecollide(sprite, group, dokill, collided = None):
    if collided is None:
        collided = collide_rect
    return pygame.sprite.spritecollide(sprite, group, dokill, collided)
