from stacked_sprite import *
from random import randint, uniform
from entity import Entity
from cache import Cache
from player import Player
import threading
import random
import os

P = 'player'
W = 'albert_wisker'
G = 'forest_guardian'
J = 'beetle'
K = 'kosjenka'
r1 = 'rune1_off'
r2 = 'rune2_off'
r3 = 'rune3_off'
F1, F2, F3, F4, F5, F6, F7, F8, F9 = 'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
T, A, B, C, BO, BM, TM, V, CK, GK = 'blue_tree','grass', 'bridge', 'grand_tree', 'bonsai', 'mali_bonsai', 'malo_drvo', 'vrba', 'carobni_kristali', 'grand_cristal'
R1, R2, R3, R4 = 'water1', 'water2', 'water3', 'water4'
M1 = 'mushroom1'
M2 = 'mushroom2'
M3 = 'mushroom3'
S = 'shop'

MAP = [
    [T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , T, T],
    [T , T , TM, TM, T , TM, T , T , TM, TM, T , TM, TM, TM, T , TM, T , T , T , TM, T, T],
    [T , T , M2, BM , A , BO , 0 , 0 , A , 0 , A , 0 , BM, 0 , BO , 0 , A , 0 , A , BM, T, T],
    [T , TM, A , 0 , 0 , 0 , A , BM , 0 , BO , 0 , A , 0 , A , 0 , BM, CK, 0 , GK, A , TM, T],
    [T , T , BM, A , S , J , 0 , A , 0 , A , 0 , A , 0 , M1 , 0 , A , 0 , K , 0 , A , TM, T],
    [T , TM, A , 0 , 0 , 0 , 0 , 0 , A , 0 , A , 0 , r1, 0 , A , CK, 0 , 0 , CK, 0 , T, T],
    [T , TM, A , BO , A , 0 , A , 0 , 0 , 0 , P , G , C , r2, 0 , 0 , A , BM, 0 , A , T, T],
    [T , T , 0 , A , 0 ,BM , 0 , A , 0 , A , 0 , A , r3, 0 , A , 0 , BM, 0 , A , 0 , TM, T],
    [V , V , A , V , V , 0 , 0 , V , 0 , 0 , A , 0 , A , 0 , 0 , A , 0 , A , 0 , BO, TM, T],
    [R1, R1, R1, R1, R1, R1, R1, R1, R1, R4, 0 , 0 , 0 , 0 , BO , 0 , A , BO, A , 0 , T, T],
    [V , V , M1, A , A , V , 0 , A , V , R3, W , 0 , V , 0 , 0 , A , 0 , 0 , A , M1 , T, T],
    [T , T , BO, F4, F8, F8, F5, 0 , A , R2, R1, B , R1, R4, 0 , 0 , V , BM, 0 , 0 , T, T],
    [T , TM, 0 , F7, F1, F1, F9, 0 , 0 , 0 , BO, 0 , 0 , R2, R1, R1, R4, 0 , BO, A , TM, T],
    [T , TM, A , F3, F6, F6, F2, 0 , BM, A , 0 , 0 , A , V , A , M2, R3, V , 0 , 0 , TM, T],
    [T , T , 0 , BM, 0 , A , BO, 0 , A , 0 , A , 0 , BO, 0 , 0 , V , R3, 0 , A , M3, TM, T],
    [T , TM, TM, T , TM, T , TM, T , TM, T , TM, T , TM, TM, BO, V , R3, V , TM, TM, T, T],
    [T , T , T , T , T , T , T , T , T , T , T , T , T , T , T , V , R3, V , T , T , T, T],
]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2


class Scene:
    def __init__(self, app):
        self.app = app
        self.transform_objects = []
        self.load_scene()
        self.app.message.set_message( self.app.player.message )
        self.app.message.active = True
        pg.mixer.init()
        try:
            pg.mixer.music.load('assets/bgm/Alchemists Oddities.mp3')
            pg.mixer.music.set_volume(0.2)
            pg.mixer.music.play(-1)
        except pg.error as e:
            print(f"Greška pri učitavanju glazbe: {e}")

    def load_scene(self):
        rand_rot = lambda: uniform(0, 360)
        rand_pos = lambda pos: pos + vec2(uniform(-0.25, 0.25))

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name == 'albert_wisker':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'forest_guardian':
                    Entity(self.app, name=name, pos=(pos-vec2(0.2,0)))
                elif name == 'beetle':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'kosjenka':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'blue_tree':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'bonsai':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'mali_bonsai':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'malo_drvo':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'vrba':
                    StackedSprite(self.app, name=name, pos=pos, rot=rand_rot())
                elif name == 'grand_tree':
                    StackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'carobni_kristali':
                    StackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'grand_cristal':
                    StackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune1_off':
                    StackedSprite(self.app, name=name, pos=pos, rot=180)
                elif name == 'rune2_off':
                    StackedSprite(self.app, name=name, pos=pos, rot=180)
                elif name == 'rune3_off':
                    StackedSprite(self.app, name=name, pos=pos, rot=180)
                elif name == 'shop':
                    StackedSprite(self.app, name=name, pos=(pos-vec2(0.3,0.5)), rot=215, collision=True)
                elif name == 'grass':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot(), collision=False)
                elif name in ['water1', 'water2', 'water3', 'water4']:
                    StackedSprite(self.app, name=name, pos=pos, rot=0, collision=True)
                elif name in ['field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9']:
                    StackedSprite(self.app, name=name, pos=pos, rot=0, collision=False)
                elif name == 'bridge':
                    StackedSprite(self.app, name=name, pos=pos, rot=0, collision=False)
                elif name:
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())

    def get_closest_object_to_player(self):
        closest = sorted(self.app.transparent_objects, key=lambda e: e.dist_to_player)
        closest[0].alpha_trigger = True
        closest[1].alpha_trigger = True

    def transform(self):
        for obj in self.transform_objects:
            obj.rot = 30 * self.app.time

    def draw(self):
        self.app.screen.fill(BG_COLOR)
        self.app.entity_group.draw(self.app.screen)
        self.app.main_group.draw(self.app.screen)
        self.app.message.draw()

    def update(self):
        self.get_closest_object_to_player()
        self.transform()




def run_in_thread(func, args=None, kwargs=None, callback=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    def wrapped_func():
        result = func(*args, **kwargs)
        if callback:
            callback()

    thread = threading.Thread(target=wrapped_func)
    thread.start()
    return thread
        
        

class LoadingScene:
    def __init__(self, app):
        self.app = app
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 16)
        self.progress = 0
        self.messages = [
            'Loading assets...',
            'Setting up player...',
            'Initializing game...',
            'Checking the weather...',
            'Thinking about the meaning of life...',
            'Resting...',
            'Contemplating life decisions...',
            'Talking to myself...',
            'Drinking coffee...',
            "Starring at my mobile...",
            "Doing nothing...",
            "A little bit more nothing...",
            'Almost done...',
            'Or not...',
            'Maybe...',
            "I have no idea what I'm doing...",
            
        ]
        self.bar_width = int( WIDTH / 3.0 )
        self.bar_height = int( HEIGHT / 56.33 )
        self.MAX = len( STACKED_SPRITE_ATTRS )
        self.done = False
        raw_bg = pg.image.load('assets/images/loading.png').convert()
        self.bg_img = pg.transform.smoothscale(raw_bg, self.app.screen.get_size())
        self.app.cache = Cache(self.app)
        self.app.cache.get_entity_sprite_cache()
        self.stacked_sprite_iterator = self.app.cache.get_stacked_sprite_cache()

    def done_cache( self ):
        self.done = True
        

    def update(self):
        counter = next(self.stacked_sprite_iterator, 'done')
        if counter == 'done':
            self.done_cache()
        
        if self.done:
            # Switch to the game scene after loading is complete
            self.app.scene = MenuScene(self.app)
        else:
            # Simulate loading progress
            self.progress = self.app.done_counter / self.MAX * len( self.messages )



    def draw(self):
        #self.app.screen.fill(BG_COLOR)
        self.app.screen.blit(self.bg_img, (0, 0))
        screen_center_x = self.app.screen.get_width() // 2
        screen_center_y = self.app.screen.get_height() // 100 * 85

        # Display the current message based on progress
        current_message_index = min(int(self.progress), len(self.messages) - 1)
        msg = self.messages[current_message_index]
        text = self.font.render(msg, True, 'white')
        text_rect = text.get_rect(center=(screen_center_x, screen_center_y + 80))
        self.app.screen.blit(text, text_rect)

        # Draw the progress bar background
        bar_bg_rect = pg.Rect(0, 0, self.bar_width, self.bar_height)
        bar_bg_rect.center = (screen_center_x, screen_center_y + 40)
        pg.draw.rect(self.app.screen, (204, 239, 253), bar_bg_rect)

        # Draw the progress bar
        progress_width = int(self.progress / len(self.messages) * self.bar_width)
        bar_rect = pg.Rect(0, 0, progress_width, self.bar_height)
        bar_rect.midleft = bar_bg_rect.midleft
        pg.draw.rect(self.app.screen, (221, 220, 79), bar_rect)

class MenuScene:
    def __init__(self, app):
        self.app = app
        raw_bg = pg.image.load('assets/images/menu.png').convert()
        self.bg_img = pg.transform.smoothscale(raw_bg, self.app.screen.get_size())

        btn_size = (250, 100)
        self.start_img = pg.transform.scale(pg.image.load('assets/buttons/start.png').convert_alpha(), btn_size)
        self.new_game_img = pg.transform.scale(pg.image.load('assets/buttons/reset.png').convert_alpha(), btn_size)
        self.quit_img = pg.transform.scale(pg.image.load('assets/buttons/exit.png').convert_alpha(), btn_size)
        
        self.start_hover_img = pg.transform.scale(pg.image.load('assets/buttons/start_hover.png').convert_alpha(), btn_size)
        self.new_hover_img = pg.transform.scale(pg.image.load('assets/buttons/reset_hover.png').convert_alpha(), btn_size)
        self.quit_hover_img = pg.transform.scale(pg.image.load('assets/buttons/exit_hover.png').convert_alpha(), btn_size)

        self.start_rect = self.start_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.5))
        self.new_game_rect = self.new_game_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.5 + 120))
        self.quit_rect = self.quit_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.5 + 240))

        pg.mixer.init()
        try:
            pg.mixer.music.load('assets/bgm/Lumereth.mp3')
            pg.mixer.music.set_volume(0.2)
            pg.mixer.music.play(-1)
        except pg.error as e:
            print(f"Greška pri učitavanju glazbe: {e}")

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        
        for event in pg.event.get(): 
            
            if event.type == pg.QUIT:
                pg.quit()
                import sys
                sys.exit()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.start_rect.collidepoint(mouse_pos):
                        self.app.player = Player(self.app)
                        self.app.scene = Scene(self.app)
                        return 

                    if self.new_game_rect.collidepoint(mouse_pos):
                        self.app.reset_for_new_game()
                        self.app.player = Player(self.app) 
                        self.app.scene = Scene(self.app)
                        return

                    if self.quit_rect.collidepoint(mouse_pos):
                        pg.quit()
                        import sys
                        sys.exit()

    def draw(self):
        self.app.screen.blit(self.bg_img, (0, 0))
        mouse_pos = pg.mouse.get_pos()

        if self.start_rect.collidepoint(mouse_pos):
            self.app.screen.blit(self.start_hover_img, self.start_rect)
        else:
            self.app.screen.blit(self.start_img, self.start_rect)

        if self.new_game_rect.collidepoint(mouse_pos):
            self.app.screen.blit(self.new_hover_img, self.new_game_rect)
        else:
            self.app.screen.blit(self.new_game_img, self.new_game_rect)

        if self.quit_rect.collidepoint(mouse_pos):
            self.app.screen.blit(self.quit_hover_img, self.quit_rect)
        else:
            self.app.screen.blit(self.quit_img, self.quit_rect)

class PauseScene:
    def __init__(self, app, game_scene):
        self.app = app
        self.game_scene = game_scene
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 40)

        self.resume_img = pg.transform.scale(pg.image.load('assets/buttons/continue.png').convert_alpha(), (250, 100))
        self.exit_img = pg.transform.scale(pg.image.load('assets/buttons/exit.png').convert_alpha(), (250, 100))

        self.resume_hover_img = pg.transform.scale(pg.image.load('assets/buttons/continue_hover.png').convert_alpha(), (250, 100))
        self.exit_hover_img = pg.transform.scale(pg.image.load('assets/buttons/exit_hover.png').convert_alpha(), (250, 100))

        self.resume_rect = self.resume_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.45))
        self.exit_rect = self.exit_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.65))

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.app.exit_game()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.app.scene = self.game_scene

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.resume_rect.collidepoint(mouse_pos):
                        self.app.scene = self.game_scene
                    elif self.exit_rect.collidepoint(mouse_pos):
                        self.app.exit_game()

    def draw(self):
        self.game_scene.draw()

        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.app.screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSE", True, 'white')
        self.app.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT * 0.25)))
        mouse_pos = pg.mouse.get_pos()

        if self.resume_rect.collidepoint(mouse_pos):
            self.app.screen.blit(self.resume_hover_img, self.resume_rect)
        else:
            self.app.screen.blit(self.resume_img, self.resume_rect)

        if self.exit_rect.collidepoint(mouse_pos):
            self.app.screen.blit(self.exit_hover_img, self.exit_rect)
        else:
            self.app.screen.blit(self.exit_img, self.exit_rect)

class ShopScene:
    def __init__(self, app, previous_scene):
        self.app = app
        self.previous_scene = previous_scene

        try:
            self.bg_img = pg.image.load('assets/images/shop_inside.png').convert()
            self.bg_img = pg.transform.smoothscale(self.bg_img, RES)
        except Exception as e:
            print(f"Greška pri učitavanju slike: {e}")
            self.bg_img = pg.Surface(RES)
            self.bg_img.fill((20, 20, 20))

        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 15)
        self.buttons_font = pg.font.Font("assets/PressStart2P-Regular.ttf", 30)
        
        self.items = [
            {"name": "Sunshroom", "price": 50, "id": "orange_mush"},
            {"name": "Moonshroom", "price": 200, "id": "blue_mush"},
            {"name": "Moon key", "price": 5000, "id": "key1"},
            {"name": "Nature key", "price": 7000, "id": "key2"},
            {"name": "Water key", "price": 10000, "id": "key3"},
        ]
        
        self.shop_rect = pg.Rect(750, 110, 420, 450)
    
        self.exit_surf = self.buttons_font.render("EXIT", True, 'white')
        self.exit_rect = self.exit_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100))

    def buy_item(self, item):
        if self.app.coins >= item['price']:
            if item['id'] in ['orange_mush', 'blue_mush']:
                self.app.coins -= item['price']
                self.app.inventory[item['id']] += 1
            elif not self.app.inventory.get(item['id']):
                self.app.coins -= item['price']
                self.app.inventory[item['id']] = True

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.app.scene = self.previous_scene
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.exit_rect.collidepoint(mouse_pos):
                        self.app.scene = self.previous_scene
                        return

                    for i, item in enumerate(self.items):
                        item_id = item['id']
                        if item_id.startswith('key') and self.app.inventory.get(item_id):
                            continue
                        
                        item_rect = pg.Rect(self.shop_rect.x + 10, self.shop_rect.y + 60 + i * 70, 400, 60)
                        if item_rect.collidepoint(mouse_pos):
                            self.buy_item(item)

    def draw(self):
        self.app.screen.blit(self.bg_img, (0, 0))
        
        coin_text = f"Coins: {self.app.coins}"
        coin_surf = self.buttons_font.render(coin_text, True, 'yellow')
        coin_shadow = self.buttons_font.render(coin_text, True, 'black')
        self.app.screen.blit(coin_shadow, (WIDTH - coin_surf.get_width() - 18, 22))
        self.app.screen.blit(coin_surf, (WIDTH - coin_surf.get_width() - 20, 20))

        mouse_pos = pg.mouse.get_pos()
        for i, item in enumerate(self.items):
            item_rect = pg.Rect(self.shop_rect.x + 10, self.shop_rect.y + 60 + i * 70, 400, 60)
            item_id = item['id']

            is_key = item_id.startswith('key')
            already_has_key = is_key and self.app.inventory.get(item_id, False)

            if already_has_key:
                bg_col, txt_col, status = (80, 0, 0), (255, 50, 50), "SOLD"
            else:
                is_hover = item_rect.collidepoint(mouse_pos)
                bg_col = (60, 60, 60) if is_hover else (30, 30, 30)
                txt_col = 'white'

                if not is_key:
                    count = self.app.inventory.get(item_id, 0)
                    status = f"{item['price']}C ({count})"
                else:
                    status = f"{item['price']}C"

            pg.draw.rect(self.app.screen, bg_col, item_rect)
            pg.draw.rect(self.app.screen, 'red' if already_has_key else 'white', item_rect, 2)
            
            name_surf = self.font.render(item['name'], True, txt_col)
            stat_surf = self.font.render(status, True, 'yellow' if not already_has_key else txt_col)
            
            self.app.screen.blit(name_surf, (item_rect.x + 15, item_rect.y + 20))
            self.app.screen.blit(stat_surf, (item_rect.right - stat_surf.get_width() - 15, item_rect.y + 20))

        exit_col = 'yellow' if self.exit_rect.collidepoint(mouse_pos) else 'white'
        exit_surf = self.buttons_font.render("EXIT", True, exit_col)
        self.app.screen.blit(exit_surf, self.exit_rect)

class FishingScene:
    def __init__(self, app, previous_scene):
        self.app = app
        self.previous_scene = previous_scene
        self.app.message.active = False
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 20)
        
        self.bar_rect = pg.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 40)
        self.green_zone = pg.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 40)
        
        self.marker_pos = self.bar_rect.left
        self.marker_speed = randint(3, 8)
        self.direction = 1
        pg.mixer.init()

    def update(self):
        self.marker_pos += self.marker_speed * self.direction
        if self.marker_pos >= self.bar_rect.right:
            self.marker_pos = self.bar_rect.right
            self.direction = -1
        elif self.marker_pos <= self.bar_rect.left:
            self.marker_pos = self.bar_rect.left
            self.direction = 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.green_zone.left <= self.marker_pos <= self.green_zone.right:
                        self.fish_reward = self.marker_speed * 2
                        self.app.coins += self.fish_reward
                        self.app.message.set_message(f"ALBERT WISKER: \nNow THAT’S a catch! You’ve got quicker hands than most travelers. + {self.fish_reward} Coins")
                        try:
                            success_sfx = pg.mixer.Sound('assets/sfx/Minigame_Success_SFX.mp3')
                            success_sfx.play(loops=0, maxtime=0, fade_ms=0)
                        except pg.error as e:
                            print(f"Greška pri učitavanju glazbe: {e}")
                    else:
                        self.app.message.set_message("ALBERT WISKER: \nPoor perofomance indeed! ")
                        try:
                            fail_sfx = pg.mixer.Sound('assets/sfx/Minigame_Fail_SFX.mp3')
                            fail_sfx.play(loops=0, maxtime=0, fade_ms=0)
                        except pg.error as e:
                            print(f"Greška pri učitavanju glazbe: {e}")
                    
                    self.app.message.active = True
                    self.app.scene = self.previous_scene
                
                elif event.key == pg.K_ESCAPE:
                    self.app.scene = self.previous_scene

    def draw(self):
        self.previous_scene.draw()
        
        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.app.screen.blit(overlay, (0, 0))

        pg.draw.rect(self.app.screen, 'red', self.bar_rect)
        pg.draw.rect(self.app.screen, 'green', self.green_zone)
        pg.draw.rect(self.app.screen, 'black', self.bar_rect, 3)
        
        pg.draw.line(self.app.screen, 'white', (self.marker_pos, self.bar_rect.top - 10), 
                     (self.marker_pos, self.bar_rect.bottom + 10), 5)
        
        txt = self.font.render("Press SPACE in the green area!", True, 'white')
        self.app.screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

class SimonSaysScene:
    def __init__(self, app, previous_scene):
        self.app = app
        self.previous_scene = previous_scene
        self.app.message.active = False
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 30)

        self.current_difficulty = self.app.simon_says_difficulty
        self.sequence = [random.choice(['W', 'A', 'S', 'D']) for _ in range(5 + self.current_difficulty)]
        self.player_input = []
        self.start_time = pg.time.get_ticks()
        self.show_duration = 4000 
        self.input_phase = False
        self.finished = False

        pg.mixer.init()

    def update(self):
        curr_time = pg.time.get_ticks()
        
        if not self.input_phase and curr_time - self.start_time > self.show_duration:
            self.input_phase = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and self.input_phase and not self.finished:
                key_name = pg.key.name(event.key).upper()
                if key_name in ['W', 'A', 'S', 'D']:
                    self.player_input.append(key_name)
                    
                    idx = len(self.player_input) - 1
                    if self.player_input[idx] != self.sequence[idx]:
                        self.fail_game()
                        self.app.message.active = True
                        self.app.scene = self.previous_scene

                    elif len(self.player_input) == len(self.sequence):
                        self.win_game()
                        self.app.message.active = True
                        self.app.scene = self.previous_scene

    def win_game(self):
        self.finished = True
        for mush in self.app.growing_mushrooms:
            elapsed = pg.time.get_ticks() - mush.plant_time
            remaining = mush.growth_time - elapsed
            mush.growth_time = elapsed + (remaining * 0)

        if self.app.simon_says_difficulty < 10:
            self.app.simon_says_difficulty += 1

        self.app.message.set_message("KOSJENKA: \nImpressive focus. Your memory grows stronger and so do your mushrooms!")
        try:
            success_sfx = pg.mixer.Sound('assets/sfx/Minigame_Success_SFX.mp3')
            success_sfx.play(loops=0, maxtime=0, fade_ms=0)
        except pg.error as e:
            print(f"Greška pri učitavanju glazbe: {e}")

    def fail_game(self):
        self.finished = True
        self.app.message.set_message("KOSJENKA: \nThe sequence faded from your mind.")
        try:
            fail_sfx = pg.mixer.Sound('assets/sfx/Minigame_Fail_SFX.mp3')
            fail_sfx.play(loops=0, maxtime=0, fade_ms=0)
        except pg.error as e:
            print(f"Greška pri učitavanju glazbe: {e}")

    def draw(self):
        self.previous_scene.draw()
        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.app.screen.blit(overlay, (0, 0))

        if not self.input_phase:
            title = self.font.render("MEMORIZE THIS:", True, 'white')
            seq_display = " ".join(self.sequence)
            seq_surf = self.font.render(seq_display, True, 'yellow')
            
            timer = 4 - (pg.time.get_ticks() - self.start_time) // 1000
            info = self.font.render(f"Starts in: {max(0, timer)}", True, 'red')
        else:
            title = self.font.render("YOUR TURN:", True, 'green')
            seq_display = " ".join(self.player_input)
            seq_surf = self.font.render(seq_display, True, 'white')
            info = self.font.render("Repeat the pattern!", True, 'gray')

        self.app.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        self.app.screen.blit(seq_surf, seq_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.app.screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))