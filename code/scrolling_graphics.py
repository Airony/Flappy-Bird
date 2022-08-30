from math import ceil, floor
import pygame
from settings import *

parts = []
class ScrollingGraphic():
    def __init__(self,size,pos_y,image,speed,group,display_surface):
        self.size = size
        count = ceil(SCREEN_WIDTH / size[0]) * 2
        self.parts = [None] * count
        self.display_surface = display_surface
        self.speed = speed

        for i in range(count):
            self.parts[i] = mySurf((i * size[0],pos_y),image,size,group,i,speed,self.move_part)
        parts = self.parts
            
        self.last_part = self.parts[count - 1]
        
    def move_part(self,i):
        self.parts[i].pos[0] = floor(self.last_part.pos[0]) + self.size[0]
        self.parts[i].rect[0] = floor(self.parts[i].pos[0])
        self.last_part = self.parts[i]
        
    def print_coords(self):
        for part in self.parts:
            part.print_pos()
        
    def draw(self):
        for part in self.parts:
            self.display_surface.blit(part.image,part.pos)
            
        
class mySurf(pygame.sprite.Sprite):
    def __init__(self,pos,image,size,group,index,speed,move_func):
        super().__init__(group)
        self.speed = speed
        self.image = pygame.image.load(image).convert()
        scaleFact = (size[0] or self.image.get_width(),size[1] or self.image.get_height())
        self.image = pygame.transform.scale(self.image,scaleFact)
        self.rect = self.image.get_rect()
        self.size = (self.rect.width,self.rect.height)
        
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pygame.math.Vector2(pos)
        
        self.index = index
        self.move_func = move_func
    
    def update(self,dt):
        if self.pos[0] + self.size[0] <= 0:
            self.move_func(self.index) 
        self.pos[0] = self.pos[0] - self.speed * dt
        self.rect.x = floor(self.pos[0])
        
        
    def print_pos(self):
        print('Left number ' + str(self.index) + ' :' + str(self.rect.left) + ' ' + str(self.pos[0]))
        print('Right number ' + str(self.index) + ' :' + str(self.rect.right) + ' ' + str(self.pos[0]))