from math import ceil, floor
import pygame
from helper import file
from events import PLAYER_DIE_EVENT,SCORE_EVENT
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group,collision_sprites,score_sprites):
        super().__init__(group)
        self.collision_sprites = collision_sprites
        self.score_sprites = score_sprites
        self.size = (51,36)
        self.animation_index = 0
        self.animation_count = len(PLAYER_ANI_FILES)
        self.animation_dir = 1
        
        self.surfaces = [None] * self.animation_count
        for i,file_name in enumerate(PLAYER_ANI_FILES):
            self.surfaces[i] = pygame.image.load(file(f'../graphics/{file_name}')).convert()
            self.surfaces[i] = pygame.transform.scale(self.surfaces[i],self.size)
        
        self.image = self.surfaces[0]
        self.orig_sprite = self.image
        self.pos = pos
        self.is_moving = False
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = pygame.Vector2(0,0)
        self.velocity = pygame.Vector2(0,0)
        
        self.rotation = 0
        
        self.score = 0
        self.score_sound = pygame.mixer.Sound(file('../audio/point.ogg'))
        self.score_sound.set_volume(0.30)
        self.jump_sound = pygame.mixer.Sound(file('../audio/swoosh.ogg'))
        self.jump_sound.set_volume(0.4)
        self.die_sound = pygame.mixer.Sound(file('../audio/die.ogg'))
        self.die_sound.set_volume(0.35)
    
    def input(self,events):
        for event in events:
            if(event.type == pygame.KEYDOWN):
                if  event.key == pygame.K_SPACE:
                    self.jump_sound.play()
                    self.velocity.y = JUMP_POWER
            
               
               
    def collision(self):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                self.die_sound.play()
                print('collided')
                pygame.event.post(PLAYER_DIE_EVENT)
                self.is_moving = False
        for sprite in self.score_sprites:
            if sprite.rect.colliderect(self.rect):
                self.score_sound.play()
                pygame.event.post(SCORE_EVENT)
                sprite.kill()
        
    def update(self,dt,events):
        self.input(events)
        if self.is_moving:
            self.move(dt)
            self.collision()
        self.animate(dt)
        
    def move(self,dt):
        self.velocity.y -=  FALL_POWER * dt 
        self.pos.y = self.pos.y - self.velocity.y * dt * PLAYER_SPEED
        self.rect.y = round(self.pos.y)
        rotation_start =  -3.5
        rotation_max = -12.5
        a = 90 / (rotation_start - rotation_max)
        b = -1 * rotation_start * a
        if(self.velocity.y > rotation_start):
            self.rotation = 30
        else:
            self.rotation = max(a * self.velocity.y + b,-90)
        self.update_rotation()
    
    def animate(self,dt):
        self.animation_index += dt * 1000 / (PLAYER_ANI_DURATION / self.animation_count) * self.animation_dir
        self.last_index = self.animation_index
        if(floor(self.animation_index) >= self.animation_count ):
            self.animation_dir = -1
            self.animation_index = self.animation_count - 1
        elif (floor(self.animation_index) < 0):
            self.animation_dir = 1
            self.animation_index = 0
        
        if (self.animation_dir > 0 and self.last_index != floor(self.animation_index)): 
            self.last_index = floor(self.animation_index)
            self.orig_sprite = self.surfaces[floor(self.animation_index)] 
            
        elif(self.animation_dir < 0 and self.last_index != ceil(self.animation_index)):
            self.last_index = ceil(self.animation_index)
            self.orig_sprite = self.surfaces[ceil(self.animation_index)] 
        self.update_rotation()
            
            
    def set_sprite(self,index):
        self.image = pygame.transform.rotate(self.surfaces[index],self.rotation)
        
    def update_rotation(self):
        self.image = pygame.transform.rotate(self.orig_sprite,self.rotation)
            
    
    def reset(self):
        self.rotation = 0
        self.pos[1] = SCREEN_HEIGHT / 2
        self.rect.y = self.pos[1]
        self.image = self.orig_sprite

    def lock(self):
        self.velocity.y = 0
        self.is_moving = False        