import sys
import platform
from settings import *
from cache import Cache
from player import Player
from scene import Scene, LoadingScene, PauseScene
import asyncio
from itertools import cycle
from message import Message
from farming import plant_mushroom
from stacked_sprite import StackedSprite
from random import uniform

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES, pg.FULLSCREEN) #
        pg.font.init()
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, 100)
        # groups
        self.main_group = pg.sprite.LayeredUpdates()
        self.entity_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.transparent_objects = []

        self.done_counter = 0
        # game objects

        self.player = None
        self.cache = None
        self.scene = LoadingScene( self )
        self.message = Message( self )

        self.coins = 0
        self.inventory = set()

        self.font_coins = pg.font.Font("assets/PressStart2P-Regular.ttf", 30)

    def update(self):
        rand_rot = lambda: uniform(0, 360)
        self.scene.update()
        self.entity_group.update()
        self.main_group.update()

        curr_time = pg.time.get_ticks()
        
        for sprite in self.main_group:
            if isinstance(sprite, StackedSprite) and sprite.name.endswith('_small'):
                if hasattr(sprite, 'growth_time'):
                    if curr_time - sprite.plant_time > sprite.growth_time:
                        pos = sprite.pos / TILE_SIZE 
                        adult_name = sprite.name.replace('_small', '')
                        sprite.kill() 
                        
                        StackedSprite(self, name=adult_name, pos=pos, rot=rand_rot(), collision=False)

        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick()

    def draw_coins(self):
        text = f"Coins: {self.coins}"
        coin_surf = self.font_coins.render(text, True, 'yellow')
        shadow_surf = self.font_coins.render(text, True, 'black')
        
        pos = (WIDTH - coin_surf.get_width() - 20, 20)
        
        self.screen.blit(shadow_surf, (pos[0] + 2, pos[1] + 2))
        self.screen.blit(coin_surf, pos)

    def draw_interaction_msg(self):
        from scene import Scene
        if not isinstance(self.scene, Scene):
            return

        for sprite in self.main_group:
            if hasattr(sprite, 'name') and sprite.name == 'shop':
                player_pos = self.player.offset
                shop_pos = sprite.pos
                dist = player_pos.distance_to(shop_pos)

                if dist < 200:
                    text = "Press 'E' to Enter Shop"
                    msg_surf = self.font_coins.render(text, True, 'white')
                    
                    pos = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT * 0.8))
                    
                    self.screen.blit(msg_surf, pos)
                    break

    def draw(self):
        try:
            self.scene.draw()
        except:
            self.screen.fill(BG_COLOR)
            self.entity_group.draw(self.screen)
            self.main_group.draw(self.screen)
            self.message.draw()
        
        if isinstance(self.scene, (Scene)):
            self.draw_coins()
            self.draw_interaction_msg()
        
        pg.display.flip()

    def check_events(self):
        from scene import ShopScene
        if isinstance(self.scene, ShopScene):
            self.scene.update()
            return
        
        self.anim_trigger = False
        if hasattr(self.scene, 'start_rect') or hasattr(self.scene, 'resume_rect'): 
            return
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif e.type == pg.KEYDOWN and e.key == pg.K_f:
                from scene import Scene
                if isinstance(self.scene, Scene):
                    plant_mushroom(self, self.scene)

            elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                from scene import Scene
                if isinstance(self.scene, Scene):
                    self.scene = PauseScene(self, self.scene)

            elif e.type == pg.KEYDOWN and e.key == pg.K_e:
                from scene import Scene, ShopScene
                if isinstance(self.scene, Scene):
                    for sprite in self.main_group:
                        if hasattr(sprite, 'name') and sprite.name == 'shop':
                            player_pos = self.player.offset
                            shop_pos = sprite.pos
                            dist = player_pos.distance_to(shop_pos)
                            
                            if dist < 200:
                                self.scene = ShopScene(self, self.scene)
                                break

            elif e.type == self.anim_event:
                self.anim_trigger = True
                
            elif e.type == pg.KEYDOWN:
                if self.player:
                    self.player.single_fire(event=e)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

async def run( app ):
    while True:
        if app.player:
            app.check_events()
        app.get_time()
        app.update()
        app.draw()
        await asyncio.sleep( 0 )


if __name__ == '__main__':
    if __import__("sys").platform == "emscripten":
        from time import sleep
        try:
            platform.document.body.style.background = '#000000'
        except:
            pass

    app = App()
    asyncio.run( run( app ) )
