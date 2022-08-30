from asyncio import events
import pygame,pygame.freetype
from settings import *
from player import Player
from obstacle import Obstacle
from scrolling_graphics import ScrollingGraphic
from helper import file
from events import PLAYER_DIE_EVENT,SCORE_EVENT
from threading import Timer

class Game:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.score_sprites = pygame.sprite.Group()
        self.setup()
        
    def setup(self):
        self.player = Player(pygame.math.Vector2(300,SCREEN_HEIGHT/2 - 32),[],self.collision_sprites,self.score_sprites)
        self.obstacles = list()
        self.background = ScrollingGraphic((SCREEN_WIDTH,SCREEN_HEIGHT),0,file('../graphics/background 5.png'),BACKGROUND_SPEED,self.all_sprites,self.display_surface)
        self.create_floor()
        self.font = pygame.font.Font(file('../graphics/fonts/Pixeltype.ttf'),60)
        self.create_start_screen()
        self.is_running = False
        self.is_fading = False
        self.display_message = True
        self.score = 0
        self.high_score = 0
        self.create_fade_screen()
        
        
    
    def create_start_screen(self):
        self.start_screen = pygame.sprite.Sprite(self.all_sprites)
        self.start_screen.image = pygame.image.load(file('../graphics/message.png')).convert_alpha()
        self.start_screen.image = pygame.transform.scale2x(self.start_screen.image)
        self.start_screen.rect = self.start_screen.image.get_rect()
        self.start_screen.rect.centerx = round(SCREEN_WIDTH / 2)
        self.start_screen.rect.centery = round(SCREEN_HEIGHT / 2)
        
    def create_fade_screen(self):
        self.fade_screen = pygame.surface.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA,32)
        self.fade_screen.convert_alpha()
        self.fade_screen.fill('black')
        
    def start_fade(self):
        self.fade_screen.set_alpha(255)
        self.alpha = 0
        self.fade_direction = 1
        self.is_fading = True
        self.fade_paused = False
        
        
    def animate_fade(self,dt):
        
        self.prev_alpha = self.alpha
        self.alpha +=  self.fade_direction *  dt * 1000 * 255 / FADE_DURATION
        clamped_alpha = max(0,min(round(self.alpha),255))
        
        if clamped_alpha == 255 and self.fade_direction > 0 and not self.fade_paused:
            self.fade_paused = True
            Timer(FADE_PAUSE / 1000 ,self.reverse_fade).start()
        elif clamped_alpha == 0 and self.fade_direction < 0:
            self.is_fading = False
            return
            
        self.fade_screen.set_alpha(clamped_alpha)
        self.display_surface.blit(self.fade_screen,(0,0))
        
    def reverse_fade(self):
        self.clean_up()
        self.fade_paused = False
        self.fade_direction = -1
        self.alpha = 255
    
    def run(self,dt,events):
        self.display_surface.fill('black')
        self.background.draw()
        self.display_surface.blit(self.player.image,self.player.pos)
        self.all_sprites.update(dt)
        self.player.update(dt,events)
        if self.is_running:
            self.update_obstacles(dt)
        self.draw_obstacles()
        self.floor.draw()
        self.render_score()
        if (self.display_message):
            self.display_surface.blit(self.start_screen.image,self.start_screen.rect)
        if self.is_fading:
            self.animate_fade(dt)
        self.listen_for_events(events)
        
    def create_floor(self):
        floor_pos = (0,SCREEN_HEIGHT - FLOOR_HEIGHT)
        self.floor = ScrollingGraphic((SCREEN_WIDTH,0),floor_pos[1],file('../graphics/floor.png'),FLOOR_SPEED,self.all_sprites,self.display_surface)
        floor_hitbox = pygame.sprite.Sprite(self.collision_sprites)
        floor_hitbox.rect = pygame.rect.Rect(floor_pos[0],floor_pos[1],SCREEN_WIDTH,FLOOR_HEIGHT)
        
    def render_score(self):
        score_ui = self.font.render(str(self.score),False,'white')
        high_score_ui = self.font.render('HI: ' + str(self.high_score),False,'white')
        self.display_surface.blit(score_ui,(20,20))
        self.display_surface.blit(high_score_ui,(SCREEN_WIDTH - 100,20))
        
    def create_obstacles(self,pos_x,color = False):
        for i in range(6):
            new_pos_x = pos_x + i * (PIPE_WIDTH + HORIZONTAL_GAP)
            obstacle = Obstacle(new_pos_x,self.collision_sprites,self.score_sprites)
            self.obstacles.append(obstacle)
            
    
    def update_obstacles(self,dt):
        for obstacle in self.obstacles:
            obstacle.update(dt)
            if(obstacle.pos_x + obstacle.width <= -1 * SCREEN_WIDTH):
                obstacle.kill();
                self.obstacles.remove(obstacle)
                
        last_obstacle = self.obstacles[len(self.obstacles) - 1]
        if(last_obstacle.pos_x <= SCREEN_WIDTH + 200):
            self.create_obstacles(last_obstacle.pos_x + PIPE_WIDTH + HORIZONTAL_GAP)
            
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw(self.display_surface)
            
        
    def print_coords(self):
        print('----------------------')
        self.background.print_coords()
        print('----------------------')
        
    def listen_for_events(self,events):
        for event in events:
            if event == PLAYER_DIE_EVENT:
                self.stop_game()
                self.start_fade()
            elif event == SCORE_EVENT:
                self.add_score()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not( self.is_running or self.is_fading) :
                    self.start_game()
                    
    def stop_game(self):
        self.player.lock()
        self.is_running = False
    
    def clean_up(self):
        self.display_message = True
        self.player.reset()
        for obstacle in self.obstacles:
            obstacle.kill()
        self.obstacles = []
        self.score = 0
        
    def start_game(self):
        self.display_message = False
        self.is_running = True
        self.player.is_moving = True
        self.create_obstacles(SCREEN_WIDTH)
        
    def add_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score