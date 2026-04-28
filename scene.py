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
R1 = 'rune1_off'
R2 = 'rune2_off'
R3 = 'rune3_off'
F1, F2, F3, F4, F5, F6, F7, F8, F9 = 'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
T, A, R, B, C = 'blue_tree','grass', 'water', 'bridge', 'grand_tree'
S = 'shop'
SP = 'sphere'

MAP = [
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],
    [T, T, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, T, T],
    [T, T, 0, 0, 0, 0, A, 0, 0, 0, A, 0, 0, 0, A, 0, 0, 0, 0, 0, T, T],
    [T, T, 0, 0, S, J, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, K, 0, 0, T, T],
    [T, T, 0, A, 0, 0, 0, 0, A, 0, 0, 0, R1, 0, 0, 0, 0, 0, 0, 0, T, T],
    [T, T, 0, 0, 0, 0, 0, 0, 0, 0, P, G, C, R2, 0, 0, 0, A, 0, 0, T, T],
    [T, T, 0, 0, A, 0, 0, 0, A, 0, 0, 0, R3, 0, 0, 0, A, 0, 0, 0, T, T],
    [T, T, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, T, T],
    [R, R, R, R, R, R, R, R, R, R, 0, 0, 0, 0, A, 0, 0, A, 0, 0, T, T],
    [T, T, 0, 0, 0, A, 0, 0, 0, R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, T, T],
    [T, T, 0, F4, F8, F8, F5, 0, 0, R, R, B, R, R, 0, 0, 0, 0, A, 0, T, T],
    [T, T, 0, F7, F1, F1, F9, 0, 0, 0, 0, 0, 0, R, R, R, R, 0, 0, 0, T, T],
    [T, T, 0, F3, F6, F6, F2, 0, 0, 0, A, 0, 0, 0, 0, 0, R, 0, 0, 0, T, T],
    [T, T, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, A, 0, 0, R, 0, 0, 0, T, T],
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, R, T, T, T, T, T],
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, R, T, T, T, T, T],
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
                    Entity(self.app, name=name, pos=pos)
                elif name == 'beetle':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'kosjenka':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'blue_tree':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'grand_tree':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune1_off':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune2_off':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=0)
                elif name == 'rune3_off':
                    TrnspStackedSprite(self.app, name=name, pos=(pos-vec2(0,0.4)), rot=0)
                elif name == 'shop':
                    StackedSprite(self.app, name=name, pos=(pos+vec2(0.3,0.5)), rot=215, collision=True)
                elif name == 'grass':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot(), collision=False)
                elif name == 'water':
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