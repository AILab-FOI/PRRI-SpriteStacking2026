from settings import *
from stacked_sprite import StackedSprite
from random import uniform, randint
import pygame as pg
from scene import MAP, F 

def plant_mushroom(app, scene):
    rand_rot = lambda: uniform(0, 360)
    grid_pos = app.player.offset / TILE_SIZE
    map_x, map_y = int(grid_pos.x), int(grid_pos.y)

    if 0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0]):
        if MAP[map_y][map_x] == F:
            existing_mush = None
            for sprite in app.main_group:
                if isinstance(sprite, StackedSprite) and 'mushroom1' in sprite.name:
                    if int(sprite.pos.x / TILE_SIZE) == map_x and int(sprite.pos.y / TILE_SIZE) == map_y:
                        existing_mush = sprite
                        break

            if existing_mush:
                if existing_mush.name == 'mushroom1':
                    existing_mush.kill()
                    app.coins += 10
                else:
                    elapsed = pg.time.get_ticks() - existing_mush.plant_time
                    remaining = max(0, int((existing_mush.growth_time - elapsed) / 1000))
            else:
                m = StackedSprite(app, name='mushroom1_small', pos=vec2(map_x, map_y) + vec2(0.5), rot=rand_rot(), collision=False)
                m.plant_time = pg.time.get_ticks() 
                m.growth_time = randint(10000, 60000) 