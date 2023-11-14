import pygame as pg
import math
from settings import *

class Raycasting:
    def __init__(self, game):
        # contructor
        self.game = game
        self.rc_result = []
        self.objects_to_render = [] # [(depth, wall_column, wall_pos), ...]
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_render(self):
        self.objects_to_render.clear()
        for ray, values in enumerate(self.rc_result):
            depth, p_height, texture, offset = values
            # If que comprueba si la pared es mas alta que la pantalla. Si es mas alta, se recorta, si no, se pinta entera
            # Esto para evitar caidas de fps
            if p_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, p_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - p_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / p_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_casting(self):
        self.rc_result.clear()
        ox, oy = self.game.player.pos
        x, y = self.game.player.map_pos

        texture_v, texture_h = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001 # 0.0001 para evitar divisiones por 0

        # Ray casting
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y + 1, 1) if sin_a > 0 else (y - 1e-6, -1)

            depth_h = (y_hor - oy) / sin_a
            x_h = ox + depth_h * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            # Comprobar si la pared horizontal esta mas cerca que la vertical
            for i in range(MAX_DEPTH):
                tile_hor = int(x_h), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_h = self.game.map.world_map[tile_hor]
                    break
                x_h += dx
                y_hor += dy
                depth_h += delta_depth

            # Verticales
            x_v, dx = (x + 1, 1) if cos_a > 0 else (x - 1e-6, -1)

            depth_v = (x_v - ox) / cos_a
            y_v = oy + depth_v * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # Comprobar si la pared vertical esta mas cerca que la horizontal
            for i in range(MAX_DEPTH):
                tile_vert = int(x_v), int(y_v)
                if tile_vert in self.game.map.world_map:
                    texture_v = self.game.map.world_map[tile_vert]
                    break
                x_v += dx
                y_v += dy
                depth_v += delta_depth


            # Elegir la pared mas cercana
            if depth_v < depth_h:
                depth, texture = depth_v, texture_v
                y_v %= 1
                offset = y_v if cos_a > 0 else (1 - y_v)
            else:
                depth, texture = depth_h, texture_h
                x_h %= 1
                offset = (1 - x_h) if sin_a > 0 else x_h

            depth *= math.cos(self.game.player.angle - ray_angle) # quitar fisheye effect

            p_height = SCREEN_DIST / (depth + 0.0001) # 0.0001 para evitar divisiones por 0

            #Pintar las paredes
            #c = [255 / (1 + depth ** 5 * 0.00002)] * 3
            #pg.draw.rect(self.game.screen, c, (ray * SCALE, HALF_HEIGHT - p_height // 2, SCALE, p_height))

            #pg.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
            #             (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            #Pintar las texturas
            self.rc_result.append((depth, p_height, texture, offset))
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_casting()
        self.get_objects_render()
