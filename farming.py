from settings import *
from stacked_sprite import StackedSprite
from random import uniform, randint
import pygame as pg
from scene import MAP, F1, F2, F3, F4, F5, F6, F7, F8, F9 

def plant_mushroom(app, scene):
    rand_rot = lambda: uniform(0, 360)
    grid_pos = app.player.offset / TILE_SIZE
    map_x, map_y = int(grid_pos.x), int(grid_pos.y)

    plant_name = 'mushroom1_small'
    reward = 10
    
    if 'blue_mush' in app.inventory:
        plant_name = 'mushroom3_small'
        reward = 25
    elif 'orange_mush' in app.inventory:
        plant_name = 'mushroom2_small'
        reward = 18

    if 0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0]):
        if MAP[map_y][map_x] in [F1, F2, F3, F4, F5, F6, F7, F8, F9]:
            existing_mush = None
            for sprite in app.main_group:
                if isinstance(sprite, StackedSprite) and 'mush' in sprite.name:
                    if int(sprite.pos.x / TILE_SIZE) == map_x and int(sprite.pos.y / TILE_SIZE) == map_y:
                        existing_mush = sprite
                        break

            if existing_mush:
                if not existing_mush.name.endswith('_small'):
                    current_reward = 10
                    if 'mushroom3' in existing_mush.name: current_reward = 30
                    elif 'mushroom2' in existing_mush.name: current_reward = 20
                    
                    existing_mush.kill()
                    app.coins += current_reward
                else:
                    print("Gljiva još raste...")
            else:
                m = StackedSprite(app, name=plant_name, pos=vec2(map_x, map_y) + vec2(0.5), rot=rand_rot(), collision=False)
                m.plant_time = pg.time.get_ticks() 
                m.growth_time = randint(5000, 15000)