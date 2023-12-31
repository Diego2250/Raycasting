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
        self.attack_sound = pg.mixer.Sound('../sounds/punch.wav')
        pg.mixer.music.set_volume(0.5)
        self.hand_sprite = pg.image.load('../sprites/doomHand.png')
        self.attack_sprite = pg.image.load('../sprites/handAttack.png')
        self.hand_sprite = pg.transform.scale(self.hand_sprite, (self.hand_sprite.get_width() * 2, self.hand_sprite.get_height() * 2))
        self.current_hand_sprite = self.hand_sprite
        self.attack_sprite = pg.transform.scale(self.attack_sprite, (self.attack_sprite.get_width() * 2, self.attack_sprite.get_height() * 2))
        self.attack_time = 0
        self.minimap_scale = 8
        self.new_game()

    def draw_minimap(self):
        for (x, y), value in self.map.world_map.items():
            rect = pg.Rect(x * self.minimap_scale, y * self.minimap_scale, self.minimap_scale, self.minimap_scale)
            if value:  # Si la celda es una pared
                pg.draw.rect(self.screen, 'white', rect)
        player_rect = pg.Rect(self.player.x * self.minimap_scale, self.player.y * self.minimap_scale, self.minimap_scale, self.minimap_scale)
        pg.draw.ellipse(self.screen, 'blue', player_rect)


    def play_music(self):
        pg.mixer.music.play(-1)

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
        if self.current_hand_sprite == self.attack_sprite:
            current_time = pg.time.get_ticks()
            if current_time - self.attack_time > 200:  # 1000 milisegundos = 1 segundo
                self.current_hand_sprite = self.hand_sprite

    def draw(self):
        #self.screen.fill('black')
        self.object_renderer.draw()
        #self.map.draw()
        #self.player.draw()
        self.draw_minimap()
        hand_x = WIDTH / 2 - self.current_hand_sprite .get_width() / 2
        hand_y = HEIGHT - self.current_hand_sprite.get_height()
        self.screen.blit(self.current_hand_sprite, (hand_x, hand_y))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # Cambiar el sprite de la mano
                if self.current_hand_sprite == self.hand_sprite:
                    self.current_hand_sprite = self.attack_sprite
                    self.current_hand_sprite = self.attack_sprite
                    self.attack_sound.play()
                    self.attack_time = pg.time.get_ticks()
                else:
                    self.current_hand_sprite = self.hand_sprite

    def run(self):
        while True:
            self.draw_minimap()
            self.check_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()