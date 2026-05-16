from settings import *
import math
from entity import BaseEntity
from itertools import cycle


class Player(BaseEntity):
    def __init__(self, app, name='player'):
        super().__init__(app, name)
        base_layer = self.images[0]
        self.mask = pg.mask.from_surface(base_layer)
        self.group.change_layer(self, CENTER.y)

        self.rect = self.image.get_rect(center=CENTER)

        self.offset = vec2(0)
        self.inc = vec2(0)
        self.prev_inc = vec2(0)
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt(2)

        self.down_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.down_list = cycle( self.down_ind )
        self.up_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.up_list = cycle( self.up_ind )
        self.left_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.left_list = cycle( self.left_ind )
        self.right_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.right_list = cycle( self.right_ind )

        self.direction = 'DOWN'
        self.moving = False

        self.message = """Welcome to the magical Forest.

Are you ready for the grand adventure?

"""

    def control(self):
        self.moving = False
        self.inc = vec2(0)
        speed = PLAYER_SPEED * self.app.delta_time
        rot_speed = PLAYER_ROT_SPEED * self.app.delta_time

        key_state = pg.key.get_pressed()

        if key_state[pg.K_LEFT]:
            self.angle += rot_speed
        if key_state[pg.K_RIGHT]:
            self.angle -= rot_speed

        if key_state[pg.K_w]:
            self.inc += vec2(0, -speed).rotate_rad(-self.angle)
            self.direction = 'UP'
            self.moving = True
        if key_state[pg.K_s]:
            self.inc += vec2(0, speed).rotate_rad(-self.angle)
            self.direction = 'DOWN'
            self.moving = True
        if key_state[pg.K_a]:
            self.inc += vec2(-speed, 0).rotate_rad(-self.angle)
            self.direction = 'LEFT'
            self.moving = True
        if key_state[pg.K_d]:
            self.inc += vec2(speed, 0).rotate_rad(-self.angle)
            self.direction = 'RIGHT'
            self.moving = True

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr

    def single_fire(self, event):
        if event.key == pg.K_SPACE:
            if self.app.message.active:
                if hasattr(self.app, 'tutorial_stage') and self.app.tutorial_stage == 0:
                    current_text = "".join(self.app.message.wrapped_text).upper()
                    if "STRIBOR" in current_text or "FOREST GUARDIAN" in current_text:
                        self.app.tutorial_stage = 1
                self.app.message.handle_input()

    def check_collision(self):
        hitobst = pg.sprite.spritecollide(self, self.app.collision_group, dokill=False, collided=pg.sprite.collide_mask)
        hit = pg.sprite.spritecollide(self, self.app.entity_group, dokill=False, collided=pg.sprite.collide_mask)
        
        if not hitobst and not hit:
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            self.inc = -self.prev_inc

    def update_mask(self):
        full_image = self.images[self.frame_index]
        mask_surf = pg.Surface(full_image.get_size(), pg.SRCALPHA)
        collision_height = 20
        rect_noge = pg.Rect(0, full_image.get_height() - collision_height, full_image.get_width(), collision_height)
        mask_surf.blit(full_image, (0, full_image.get_height() - collision_height), rect_noge)
        self.mask = pg.mask.from_surface(mask_surf)
        self.image = full_image 
        self.rect = self.image.get_rect(center=CENTER)

    def animate(self):
        if self.app.anim_trigger:
            if self.direction == 'DOWN':
                if self.moving:
                    self.frame_index = next( self.down_list )
                else:
                    self.frame_index = self.down_ind[ 1 ]
            elif self.direction == 'UP':
                if self.moving:
                    self.frame_index = next( self.up_list )
                else:
                    self.frame_index = self.up_ind[ 1 ]
            elif self.direction == 'LEFT':
                if self.moving:
                    self.frame_index = next( self.left_list )
                else:
                    self.frame_index = self.left_ind[ 1 ]
            else:
                if self.moving:
                    self.frame_index = next( self.right_list )
                else:
                    self.frame_index = self.right_ind[ 1 ]

            self.image = self.images[self.frame_index]
            self.update_mask()

    def update(self):
        if self.app.message.active:
            self.moving = False
            self.inc = vec2(0)  # Zaustavi kretanje vectorski
            self.animate()      # Pokreni animaciju stajanja (ovo radi jer smo unutar Player klase!)
            return
        
        #super().update()
        self.animate()
        self.control()
        self.check_collision()
        self.move()

    def move(self):
        self.offset += self.inc
















