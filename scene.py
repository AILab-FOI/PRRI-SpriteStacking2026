from stacked_sprite import *
from random import uniform
from entity import Entity
from cache import Cache
from player import Player
import threading

P = 'player'
W = 'albert_wisker'
G = 'forest_guardian'
J = 'beetle'
K = 'kosjenka'
r1 = 'rune1_off'
r2 = 'rune2_off'
r3 = 'rune3_off'
F1, F2, F3, F4, F5, F6, F7, F8, F9 = 'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
T, A, B, C, BO, BM, TM, V, CK = 'blue_tree','grass', 'bridge', 'grand_tree', 'bonsai', 'mali_bonsai', 'malo_drvo', 'vrba', 'carobni_kristali'
R1, R2, R3, R4 = 'water1', 'water2', 'water3', 'water4'
S = 'shop'
SP = 'sphere'

MAP = [
    [T, T, T, T, T, T, T, V, T, T, T, T, T, V, T, T, T, T, T, T, T, T],
    [V, T, T, T, T, V, T, T, T, T, V, T, T, T, T, T, V, T, T, T, T, T],
    [T, T, 0, BM, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, T, T],
    [T, V, 0, 0, 0, 0, A, 0, BO, 0, A, 0, 0, 0, A, 0, CK, 0, 0, 0, T, T],
    [T, T, 0, 0, S, J, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, K, 0, 0, T, V],
    [V, T, 0, A, 0, 0, 0, 0, A, 0, 0, 0, r1, 0, 0, CK, 0, 0, CK, 0, T, T],
    [T, T, 0, 0, 0, 0, BO, 0, 0, 0, P, G, C, r2, 0, 0, 0, A, 0, 0, V, T],
    [T, V, 0, 0, A, 0, 0, 0, A, 0, 0, 0, r3, 0, 0, 0, A, 0, 0, 0, V, T],
    [T, T, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, TM, 0, T, T],
    [R1, R1, R1, R1, R1, R1, R1, R1, R1, R4, 0, 0, 0, 0, A, 0, 0, A, 0, 0, T, T],
    [T, T, 0, 0, 0, A, 0, 0, 0, R3, W, 0, 0, 0, 0, 0, 0, 0, BO, 0, T, T],
    [T, V, 0, F4, F8, F8, F5, 0, 0, R2, R1, B, R1, R4, 0, 0, 0, 0, A, 0, T, T],
    [T, T, 0, F7, F1, F1, F9, 0, 0, 0, 0, 0, 0, R2, R1, R1, R4, 0, 0, 0, T, T],
    [T, T, 0, F3, F6, F6, F2, 0, 0, 0, A, 0, 0, 0, TM, 0, R3, 0, 0, 0, V, T],
    [T, V, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, A, 0, 0, R3, 0, 0, 0, T, T],
    [T, T, T, T, V, T, T, T, T, T, T, V, T, V, T, T, R3, T, V, T, V, T],
    [T, T, T, T, T, T, V, T, V, T, T, T, T, T, T, T, R3, T, T, T, T, T],
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
            pg.mixer.music.set_volume(0.1)
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
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'bonsai':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'mali_bonsai':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'malo_drvo':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'vrba':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'grand_tree':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'carobni_kristali':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune1_off':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune2_off':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune3_off':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
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
                elif name == 'sphere':
                    obj = StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                    self.transform_objects.append(obj)
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
        self.bg_img = pg.image.load('assets/images/loading.png')
        self.bg_img = pg.transform.smoothscale( self.bg_img, self.app.screen.get_size())
        self.app.screen.blit(self.bg_img, self.bg_img.get_rect())
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
        self.bg_img = pg.image.load('assets/images/menu.png').convert()
        self.bg_img = pg.transform.smoothscale(self.bg_img, self.app.screen.get_size())

        self.start_img = pg.image.load('assets/buttons/start.png').convert_alpha()
        self.quit_img = pg.image.load('assets/buttons/exit.png').convert_alpha()

        self.start_hover_img = pg.image.load('assets/buttons/start_hover.png').convert_alpha()
        self.quit_hover_img = pg.image.load('assets/buttons/exit_hover.png').convert_alpha()

        self.start_img = pg.transform.scale(self.start_img, (250, 100))
        self.quit_img = pg.transform.scale(self.quit_img, (250, 100))

        self.start_hover_img = pg.transform.scale(self.start_hover_img, (250, 100))
        self.quit_hover_img = pg.transform.scale(self.quit_hover_img, (250, 100))
        
        self.start_rect = self.start_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.6))
        self.quit_rect = self.quit_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.6 + 150))

        pg.mixer.init()
        try:
            pg.mixer.music.load('assets/bgm/Lumereth.mp3')
            pg.mixer.music.set_volume(0.1)
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
                pg.QUIT()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.app.scene = self.game_scene

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.resume_rect.collidepoint(mouse_pos):
                        self.app.scene = self.game_scene
                    elif self.exit_rect.collidepoint(mouse_pos):
                        pg.quit()
                        sys.exit()

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

        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.buttons_font = pg.font.Font("assets/PressStart2P-Regular.ttf", 30)
        
        self.items = [
            {"name": "Gljiva 1", "price": 10, "id": "orange_mush"},
            {"name": "Gljiva 2", "price": 15, "id": "blue_mush"},
            {"name": "Runa 1", "price": 50, "id": "key1"},
            {"name": "Runa 2", "price": 100, "id": "key2"},
            {"name": "Runa 3", "price": 150, "id": "key3"},
        ]
        
        self.shop_rect = pg.Rect(760, 110, 400, 450)
    
        self.exit_surf = self.buttons_font.render("EXIT", True, 'white')
        self.exit_rect = self.exit_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100))

    def buy_item(self, item):
        if item['id'] in self.app.inventory: return
        if self.app.coins >= item['price']:
            self.app.coins -= item['price']
            self.app.inventory.add(item['id'])

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.exit_rect.collidepoint(mouse_pos):
                        self.app.scene = self.previous_scene
                        return

                    for i, item in enumerate(self.items):
                        if item['id'] in self.app.inventory: continue
                        
                        item_rect = pg.Rect(self.shop_rect.x + 10, self.shop_rect.y + 60 + i * 70, 380, 60)
                        if item_rect.collidepoint(mouse_pos):
                            self.buy_item(item)

    def draw(self):
        self.app.screen.blit(self.bg_img, (0, 0))
        
        coin_surf = self.buttons_font.render(f"Coins: {self.app.coins}", True, 'yellow')
        shadow_surf = self.buttons_font.render(f"Coins: {self.app.coins}", True, 'black')
        Cpos = (WIDTH - coin_surf.get_width() - 20, 20)

        self.app.screen.blit(shadow_surf, (Cpos[0] + 2, Cpos[1] + 2))
        self.app.screen.blit(coin_surf, Cpos)

        mouse_pos = pg.mouse.get_pos()
        for i, item in enumerate(self.items):
            item_rect = pg.Rect(self.shop_rect.x + 10, self.shop_rect.y + 60 + i * 70, 380, 60)
            
            bought = item['id'] in self.app.inventory
            if bought:
                bg_col, txt_col, status = (80, 0, 0), (255, 50, 50), "SOLD"
            else:
                is_hover = item_rect.collidepoint(mouse_pos)
                bg_col = (60, 60, 60) if is_hover else (30, 30, 30)
                txt_col, status = 'white', f"{item['price']} C"

            pg.draw.rect(self.app.screen, bg_col, item_rect)
            pg.draw.rect(self.app.screen, 'red' if bought else 'white', item_rect, 2)
            
            name_s = self.font.render(item['name'], True, txt_col)
            stat_s = self.font.render(status, True, 'yellow' if not bought else txt_col)
            
            self.app.screen.blit(name_s, (item_rect.x + 15, item_rect.y + 20))
            self.app.screen.blit(stat_s, (item_rect.right - stat_s.get_width() - 15, item_rect.y + 20))

        exit_col = 'yellow' if self.exit_rect.collidepoint(mouse_pos) else 'white'
        exit_s = self.buttons_font.render("EXIT", True, exit_col)
        self.app.screen.blit(exit_s, self.exit_rect)