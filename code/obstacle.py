import random
import pygame
from settings import *
from helper import file

class Obstacle:
    def __init__(self,pos_x,collision_sprites,score_sprites):
        self.pos_x = pos_x
        self.width = PIPE_WIDTH
        self.collision_sprites = collision_sprites
        self.score_sprites = score_sprites
        self.create_sprites()
        
    def create_sprites(self):
        # top_pipe_size = (PIPE_WIDTH,random.randint(200,PIPE_HEIGHT - VERTICAL_GAP - FLOOR_HEIGHT))
        top_pipe_size = (PIPE_WIDTH,random.choice([150,200,250,300,350,400]))
        top_pipe_pos = pygame.math.Vector2(self.pos_x,0 - PIPE_HEIGHT + top_pipe_size[1])
        self.top_pipe = Pipe(top_pipe_pos,True,self.collision_sprites)
        
        bottom_pipe_size = (self.width,SCREEN_HEIGHT - top_pipe_size[1] - VERTICAL_GAP)
        bottom_pipe_pos = pygame.math.Vector2(self.pos_x,SCREEN_HEIGHT - bottom_pipe_size[1])
        self.bottom_pipe = Pipe(bottom_pipe_pos,False,self.collision_sprites)
        
        score_size = (2, VERTICAL_GAP)
        score_pos = pygame.math.Vector2(self.pos_x + self.width - 2 ,bottom_pipe_pos[1] - score_size[1])
        self.score_box = ScoreBox(score_pos,score_size,self.score_sprites)
        
    def update(self,dt):
        self.pos_x -= PIPE_SCROLL_SPEED * dt
        self.top_pipe.update(self.pos_x)
        self.bottom_pipe.update(self.pos_x)
        self.score_box.update(dt)
        
    def kill(self):
        self.top_pipe.kill()
        self.bottom_pipe.kill()
        self.score_box.kill()
        del self
            
    def draw(self,surface):
        surface.blit(self.top_pipe.image,self.top_pipe.pos)
        surface.blit(self.bottom_pipe.image,self.bottom_pipe.pos)
        
class ScoreBox(pygame.sprite.Sprite):
    def __init__(self,pos,size,group):
        super().__init__(group)
        self.pos = pos
        self.rect = pygame.rect.Rect(pos[0],pos[1],size[0],size[1])
        
    def update(self,dt):
        self.pos[0] -= PIPE_SCROLL_SPEED * dt
        self.rect.x = round(self.pos[0])
        
    def kill(self):
        super().kill()
        del self
        
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self,pos,flip,group):
        super().__init__(group)
        self.image = pygame.image.load(file('../graphics/pipe-green.png')).convert()
        self.image = pygame.transform.scale2x(self.image)
        if(flip):
            self.image = pygame.transform.flip(self.image,False,True)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def update(self,pos_x):
        self.pos[0] = pos_x
        self.rect.x = round(self.pos[0])
            
        
    def kill(self):
        super().kill()
        del self