import pygame as pg

_ = False

# Mapa del juego
mini_map = [
    [1, 4, 1, 4, 4, 1, 7, 1, 4, 7, 1, 7, 1, 4, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [7, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 5, 5, 5, 5, _, _, 6, 6, 6, 6, _, 4],
    [7, _, _, _, _, _, 5, _, _, _, _, _, 6, _, 1],
    [8, _, _, _, _, _, 5, _, _, _, _, _, 6, _, 4],
    [4, _, _, _, 5, 5, 5, _, _, _, _, _, 6, _, 7],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 1, _, _, _, _, _, 4],
    [1, _, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
    [1, 1, 4, 7, 1, 4, 1, 1, 1, 7, 1, 4, 7, 4, 1]
]

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgrey', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
        for pos in self.world_map]