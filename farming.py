from settings import *
from stacked_sprite import StackedSprite
from random import uniform, randint
import pygame as pg
from scene import MAP, F1, F2, F3, F4, F5, F6, F7, F8, F9 

def plant_mushroom(app, scene):
    rand_rot = lambda: uniform(0, 360)
    grid_pos = app.player.offset / TILE_SIZE
    map_x, map_y = int(grid_pos.x), int(grid_pos.y)

    existing_mush = None
    for sprite in app.main_group:
        if isinstance(sprite, StackedSprite) and 'mush' in sprite.name:
            if int(sprite.pos.x / TILE_SIZE) == map_x and int(sprite.pos.y / TILE_SIZE) == map_y:
                existing_mush = sprite
                break

    if existing_mush:
        if not existing_mush.name.endswith('_small'):
            current_reward = 10
            if 'mushroom3' in existing_mush.name: current_reward = 250
            elif 'mushroom2' in existing_mush.name: current_reward = 75
            
            existing_mush.kill()
            pg.mixer.init()
            try:
                collect_sfx = pg.mixer.Sound('assets/sfx/Mushroom_Collect_SFX.mp3')
                collect_sfx.play(loops=0, maxtime=0, fade_ms=0)
            except pg.error as e:
                print(f"Greška pri učitavanju glazbe: {e}")
            app.coins += current_reward
            return

    if 0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0]):
        if MAP[map_y][map_x] in [F1, F2, F3, F4, F5, F6, F7, F8, F9]:

            if not existing_mush:
                plant_name = 'mushroom1_small'
                if app.inventory.get('blue_mush', 0) > 0:
                    plant_name = 'mushroom3_small'
                    app.inventory['blue_mush'] -= 1
                elif app.inventory.get('orange_mush', 0) > 0:
                    plant_name = 'mushroom2_small'
                    app.inventory['orange_mush'] -= 1
                
                m = StackedSprite(app, name=plant_name, pos=vec2(map_x, map_y) + vec2(0.5), rot=rand_rot(), collision=False)
                m.plant_time = app.curr_time
                m.growth_time = randint(300000, 900000)
                app.growing_mushrooms.append(m)