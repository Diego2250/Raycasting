import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky = self.get_texture('../textures/3.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0


    def draw(self):
        self.draw_sky()
        self.render_game_objects()

    def draw_sky(self):
        # Calcular el offset con respecto al movimiento del jugador
        self.sky_offset = (self.sky_offset + 80.0 * self.game.player.angular_velocity) % WIDTH

        # SKY
        self.screen.blit(self.sky, (-self.sky_offset, 0))
        self.screen.blit(self.sky, (-self.sky_offset + WIDTH, 0))

        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))



    def render_game_objects(self):
        list_objects = self.game.raycasting.objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)



    # metodo estatico para cargar texturas
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('../textures/1.png'),
            2: self.get_texture('../textures/2.jpg'),
            3: self.get_texture('../textures/3.png'),
            4: self.get_texture('../textures/4.png'),
            5: self.get_texture('../textures/5.png'),
            6: self.get_texture('../textures/6.png'),
            7: self.get_texture('../textures/7.png'),
            8: self.get_texture('../textures/8.png'),
        }
