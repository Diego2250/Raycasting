from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.angular_velocity = 0.0
        self.rel = 0
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.footstep_sound = pg.mixer.Sound('../sounds/footsteps.wav')
        self.last_footstep_time = 0

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        time_now = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
            if time_now - self.last_footstep_time > 300:  # Ajusta la demora según tus preferencias
                self.footstep_sound.play()
                self.last_footstep_time = time_now
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
            if time_now - self.last_footstep_time > 300:
                self.footstep_sound.play()
                self.last_footstep_time = time_now
        if keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
            if time_now - self.last_footstep_time > 300:
                self.footstep_sound.play()
                self.last_footstep_time = time_now
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos
            if time_now - self.last_footstep_time > 300:
                self.footstep_sound.play()
                self.last_footstep_time = time_now

        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED * self.game.delta_time
        self.angle %= math.tau




    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy


    def draw(self):
        #pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #            (self.x * 100 + WIDTH * math.cos(self.angle),
        #             self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'blue', (int(self.x * 100), int(self.y * 100)), 12)

    def calculate_angular_velocity(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.angular_velocity = -PLAYER_ROTATION_SPEED * self.game.delta_time
        elif keys[pg.K_RIGHT]:
            self.angular_velocity = PLAYER_ROTATION_SPEED * self.game.delta_time
        else:
            self.angular_velocity = 0.0

    def update(self):
        self.movement()
        self.calculate_angular_velocity()

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)