import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.delta_time = 1
        pg.mixer.music.load('../sounds/soundtrack.mp3')
        pg.mixer.music.set_volume(0.7)
        self.new_game()

    def play_music(self):
        pg.mixer.music.play()

    def stop_music(self):
        pg.mixer.music.stop()

    def new_game(self):
        self.play_music()
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)


    def update(self):
        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')

    def draw(self):
        #self.screen.fill('black')
        self.object_renderer.draw()
        #self.map.draw()
        #self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()