import pygame as pg
import sys

vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = vec2(1600, 900)
# RES = WIDTH, HEIGHT = vec2(1920, 1080)
CENTER = H_WIDTH, H_HEIGHT = RES // 2
TILE_SIZE = 250  #

PLAYER_SPEED = 0.4
PLAYER_ROT_SPEED = 0.0015

BG_COLOR = 'olivedrab'  #
NUM_ANGLES = 72  # multiple of 360 -> 24, 30, 36, 40, 45, 60, 72, 90, 120, 180

# entity settings
ENTITY_SPRITE_ATTRS = {
    'player': {
        'path': 'assets/entities/player/player_m.png',
        'mask_path': 'assets/entities/player/mask.png',
        'num_layers': 11,
        'scale': 0.3,
        'y_offset': 0,
    },
    'albert_wisker': {
        'path': 'assets/entities/albert_wisker/albert_w.png',
        'num_layers': 12,
        'scale': 0.3,
        'y_offset': -20,
	'message':"""7 minutes. 7 minutes is all I can spare to fish with you! """
    },
    'forest_guardian': {
        'path': 'assets/entities/forest_guardian/forest_guard.png',
        'num_layers': 15,
        'scale': 0.3,
        'y_offset': -20,
	'message':"""I am the guardian of this forest! """
    },
    'beetle': {
        'path': 'assets/entities/beetle/beetle.png',
        'num_layers': 12,
        'scale': 0.3,
        'y_offset': -20,
	'message':"""Hello! """
    },
    'kosjenka': {
        'path': 'assets/entities/kosjenka/fairy.png',
        'num_layers': 12,
        'scale': 0.3,
        'y_offset': -20,
	'message':"""Hello! """
    },
    'explosion': {
        'num_layers': 7,
        'scale': 1.0,
        'path': 'assets/entities/explosion/explosion.png',
        'y_offset': 50,
    },
    'bullet': {
        'num_layers': 1,
        'scale': 0.4,
        'path': 'assets/entities/bullet/bullet.png',
        'y_offset': 50,
    },
}

# stacked sprites settings
'''mask_layer - index of the layer from which we get the mask for collisions 
and is also cached for all angles of the object, set manually or by default 
equal to num_layer // 2'''

STACKED_SPRITE_ATTRS = {
    'sphere': {
        'path': 'assets/stacked_sprites/sphere.png',
        'num_layers': 13,
        'scale': 10,
        'y_offset': 0,
        'mask_layer': 4,
    },
    'grass': {
        'path': 'assets/stacked_sprites/grass/grass.png',
        'num_layers': 11,
        'scale': 7,
        'y_offset': 20,
        'outline': False,
    },
    'blue_tree': {
        'path': 'assets/stacked_sprites/trees/blue_tree.png',
        'num_layers': 43,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
    },
    'grand_tree': {
        'path': 'assets/stacked_sprites/trees/grand_tree.png',
        'num_layers': 61,
        'scale': 7,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 2,
    },
    'water':{
        'path': 'assets/stacked_sprites/terrain/water.png',
        'num_layers': 1,
        'scale': 1,
        'y_offset': 0,
        'outline': False,
    },
    'field':{
        'path': 'assets/stacked_sprites/terrain/field.png',
        'num_layers': 1,
        'scale': 1,
        'y_offset': 0,
        'outline': False,
    },
    'bridge':{
        'path': 'assets/stacked_sprites/terrain/bridge.png',
        'num_layers': 1,
        'scale': 1,
        'y_offset': 0,
        'outline': False,
    },
    'mushroom1': {
        'path': 'assets/stacked_sprites/mushroom/mushroom1.png',
        'num_layers': 14,
        'scale': 4,
        'y_offset': 0,
        'mask_layer': 3,
        'transparency': True,
    },
    'rune1_off': {
        'path': 'assets/stacked_sprites/runes/rune1_off.png',
        'num_layers': 16,
        'scale': 4,
        'y_offset': 0,
        'mask_layer': 1,
        'transparency': True,
    },
    'rune2_off': {
        'path': 'assets/stacked_sprites/runes/rune2_off.png',
        'num_layers': 16,
        'scale': 4,
        'y_offset': 0,
        'mask_layer': 1,
        'transparency': True,
    },
    'rune3_off': {
        'path': 'assets/stacked_sprites/runes/rune3_off.png',
        'num_layers': 16,
        'scale': 4,
        'y_offset': 0,
        'mask_layer': 1,
        'transparency': True,
    },
    'shop': {
        'path': 'assets/stacked_sprites/shop/shop.png',
        'num_layers': 40,
        'scale': 4,
        'y_offset': -30,
        'mask_layer': 1,
        'transparency': True,
    },
}