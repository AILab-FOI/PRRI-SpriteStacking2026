from settings import *
from stacked_sprite import StackedSprite
from random import uniform

def plant_mushroom(app, scene):
    grid_pos = app.player.offset / TILE_SIZE
    map_x, map_y = int(grid_pos.x), int(grid_pos.y)

    from scene import MAP, F 

    if 0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0]):
        if MAP[map_y][map_x] == F:
            existing_mushroom = None
            for sprite in app.main_group:
                if isinstance(sprite, StackedSprite) and sprite.name == 'mushroom1':
                    sprite_grid_x = int(sprite.pos.x / TILE_SIZE)
                    sprite_grid_y = int(sprite.pos.y / TILE_SIZE)
                    
                    if sprite_grid_x == map_x and sprite_grid_y == map_y:
                        existing_mushroom = sprite
                        break

            if existing_mushroom:
                existing_mushroom.kill() 
            else:
                pos = vec2(map_x, map_y) + vec2(0.5)
                StackedSprite(app, name='mushroom1', pos=pos, rot=uniform(0, 360), collision=False)