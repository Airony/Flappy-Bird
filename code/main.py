import pygame,time
from sys import exit
from pygame.locals import *
from events import PLAYER_DIE_EVENT
from settings import *
from game import Game

size = (SCREEN_WIDTH,SCREEN_HEIGHT)
title = 'Flappy Snake'

class App:
    def __init__(self):
        pygame.init()
        self._running = True
        self._display_surf = None
        self.size = size
        self._display_surf = pygame.display.set_mode(self.size,pygame.HWSURFACE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.previous_time = time.time()
        
    def on_execute(self):
        while self._running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_NUMLOCK:
                        self._running= False
                        break;
             
            self.clock.tick(60)
            dt =  min(time.time() - self.previous_time,0.017)
            self.previous_time = time.time()
            self.game.run(dt,events)
            pygame.display.update()
        input()
    
if __name__ == "__main__":
    theApp = App();
    theApp.on_execute();

