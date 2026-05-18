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
from entity import Entity
from random import choice, uniform, random, randint
import random
import math
import json

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

        self.curr_time = 0
        self.play_time = 0
        self.coins = 0
        self.simon_says_difficulty = 0
        self.all_runes_active = False
        self.inventory = { 'orange_mush': 0, 'blue_mush': 0, 'key1': False, 'key2': False, 'key3': False, 'old_book': False,}
        self.konami_code = [pg.K_UP, pg.K_UP, pg.K_DOWN, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_LEFT, pg.K_RIGHT, pg.K_b, pg.K_a]
        self.current_input = []

        self.tutorial_stage = 0
        self.tasks = [
            "Talk to Stribor",
            "Go to the field and plant some mushrooms",
            "Find Kosjenka and complete the memory game",
            "Harvest the mushrooms",
            "Collect 100 coins",
            "Find Lesij's shop and buy new mushrooms",
            "Collect 1000 coins",
            "Buy the Moon key from Lesij",
            "Activate the ancient run",
            "Activate rest of the runes (1/3)",
            "Activate rest of the runes (2/3)"
        ]

        self.growing_mushrooms = []

        self.stars = []

        for _ in range(60):
            w_int = int(WIDTH)
            h_int = int(HEIGHT)

            margin = 150
    
            if random.random() > 0.5:
                x = random.choice([random.randint(0, margin), random.randint(w_int - margin, w_int)])
                y = random.randint(0, h_int)
            else:
                x = random.randint(0, w_int)
                y = random.choice([random.randint(0, margin), random.randint(h_int - margin, h_int)])
    
            self.stars.append({
                'pos': [x, y],
                'size': random.randint(3, 5),
                'speed': random.uniform(0.003, 0.006)
            })

        self.font_coins = pg.font.Font("assets/PressStart2P-Regular.ttf", 30)

        self.load_game()

    def save_game(self):
        try:
            from scene import MAP, F1, F2, F3, F4, F5, F6, F7, F8, F9
            farming_fields = [F1, F2, F3, F4, F5, F6, F7, F8, F9]
            
            mushrooms_on_fields = []
            active_runes = []
            grown_tree = []
            
            for sprite in self.main_group:
                if hasattr(sprite, 'name'):
                    if 'mush' in sprite.name:
                        map_x = int(sprite.pos.x / TILE_SIZE)
                        map_y = int(sprite.pos.y / TILE_SIZE)
                        
                        if 0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0]):
                            if MAP[map_y][map_x] in farming_fields:
                                mushrooms_on_fields.append({
                                    'name': sprite.name,
                                    'pos': [map_x, map_y],
                                    'rot': getattr(sprite, 'rot', 0),
                                    'growth_time': getattr(sprite, 'growth_time', 0),
                                    'plant_time': getattr(sprite, 'plant_time', 0)
                                })

                    elif sprite.name in ['rune1_on', 'rune2_on', 'rune3_on']:
                        active_runes.append({
                            'name': sprite.name
                        })

                    elif sprite.name == 'grand_tree_grown':
                        grown_tree.append({
                            'name': sprite.name
                        })

            save_data = {
                'play_time': self.curr_time,
                'tutorial_stage': self.tutorial_stage,
                'coins': self.coins,
                'inventory': self.inventory,
                'simon_says_difficulty': self.simon_says_difficulty,
                'player_pos': [self.player.offset.x, self.player.offset.y] if self.player else [0, 0],
                'mushrooms': mushrooms_on_fields,
                'active_runes': active_runes,
                'grown_tree': grown_tree,
                'all_runes_active': self.all_runes_active
            }

            with open('savegame.json', 'w') as f:
                json.dump(save_data, f, indent=4)
            print("Igra spremljena")
        except Exception as e:
            print(f"Greška pri spremanju: {e}")

    def load_game(self):
        import os
        if not os.path.exists('savegame.json'): return

        try:
            with open('savegame.json', 'r') as f:
                save_data = json.load(f)
                self.play_time = save_data.get('play_time', 0)
                self.tutorial_stage = save_data.get('tutorial_stage', 0)
                self.coins = save_data.get('coins', 0)
                self.inventory = save_data.get('inventory', self.inventory)
                self.simon_says_difficulty = save_data.get('simon_says_difficulty', 0)
                self.saved_player_pos = save_data.get('player_pos', None)
                self.saved_mushrooms = save_data.get('mushrooms', [])
                self.saved_runes = save_data.get('active_runes', [])
                self.grown_tree = save_data.get('grown_tree', [])
                self.all_runes_active = save_data.get('all_runes_active', None)

            print("Sustav: Podaci uspješno učitani.")
        except Exception as e:
            print(f"Greška pri učitavanju: {e}")

    def reset_for_new_game(self):
        import os
        if os.path.exists('savegame.json'):
            os.remove('savegame.json')
    
        self.play_time = 0
        self.tutorial_stage = 0
        self.coins = 0
        self.all_runes_active = False
        self.inventory = { 'orange_mush': 0, 'blue_mush': 0, 'key1': False, 'key2': False, 'key3': False, 'old_book': False}
        self.simon_says_difficulty = 0
        self.saved_player_pos = None
        self.saved_mushrooms = []
        self.saved_runes = []
        self.growing_mushrooms = []
        self.grown_tree = []

    def exit_game(self):
        print("Spremanje i izlaz...")
        self.save_game()
        pg.quit()
        sys.exit()

    def update(self):
        from scene import Scene
        if isinstance(self.scene, Scene):
            self.entity_group.update()
            self.main_group.update()
            for obj in self.transparent_objects:
                obj.alpha_trigger = True
            if hasattr(self, 'tutorial_stage'):
                if self.tutorial_stage == 4 and self.coins >= 100:
                    self.tutorial_stage = 5
                    app.message.set_message("STRIBOR: \nNow that you have some coins, visit Lesij's shop and buy some new mushrooms to plant.")
                    app.message.active = True
                elif self.tutorial_stage == 6 and self.coins >= 1000:
                    self.tutorial_stage = 7
                    app.message.set_message("STRIBOR: \nGreat job! You should now have enough coins to buy the Moon key and activate your first rune.")
                    app.message.active = True
        else:
            self.scene.update()

            if hasattr(self, 'saved_player_pos') and self.saved_player_pos and self.player:
                self.player.offset = pg.math.Vector2(self.saved_player_pos[0], self.saved_player_pos[1])
                self.saved_player_pos = None

            if hasattr(self, 'saved_mushrooms') and self.saved_mushrooms and self.player:
                for m in self.saved_mushrooms:
                    new_mush = StackedSprite(self, name=m['name'], pos=vec2(m['pos'][0] + 0.5, m['pos'][1] + 0.5), collision = False)
                    if 'growth_time' and 'plant_time' in m:
                        new_mush.growth_time = m['growth_time']
                        new_mush.plant_time = m['plant_time']
                    self.growing_mushrooms.append(new_mush)
                self.saved_mushrooms = []

            if hasattr(self, 'saved_runes') and self.saved_runes:
                if len(self.main_group) > 0:
                    for r in self.saved_runes:
                        for sprite in list(self.main_group):
                            if hasattr(sprite, 'name') and 'rune' in sprite.name:
                                r_base = r['name'].split('_')[0]
                                s_base = sprite.name.split('_')[0]
                
                                if r_base == s_base:
                                    StackedSprite(self, name=r['name'], pos=sprite.pos / TILE_SIZE, rot=180)
                                    sprite.kill()
                    self.saved_runes = []

            if hasattr(self, 'grown_tree') and self.grown_tree:
                if len(self.main_group) > 0:
                    for g in self.grown_tree:
                        for sprite in list(self.main_group):
                            if hasattr(sprite, 'name') and sprite.name == 'grand_tree':
                                StackedSprite(self, name=g['name'], pos=sprite.pos / TILE_SIZE, rot=sprite.rot)
                                sprite.kill()
                    self.grown_tree = []

        self.curr_time = self.play_time + pg.time.get_ticks()

        if self.all_runes_active:
            for sprite in self.entity_group:
                if hasattr(sprite, 'name') and sprite.name == 'kosjenka':
                    Entity(self, name='kosjenka_hair', pos=sprite.pos / TILE_SIZE)
                    sprite.kill()
                elif hasattr(sprite, 'name') and sprite.name == 'forest_guardian':
                    Entity(self, name='forest_guardian_end', pos=sprite.pos / TILE_SIZE)
                    sprite.kill()
                elif hasattr(sprite, 'name') and sprite.name == 'albert_wisker':
                    Entity(self, name='albert_wisker_end', pos=sprite.pos / TILE_SIZE)
                    sprite.kill()
                elif hasattr(sprite, 'name') and sprite.name == 'beetle':
                    Entity(self, name='beetle_end', pos=sprite.pos / TILE_SIZE)
                    sprite.kill()
        
        for sprite in self.growing_mushrooms[:]:
            if self.curr_time - sprite.plant_time > sprite.growth_time:
                pos = sprite.pos / TILE_SIZE 
                adult_name = sprite.name.replace('_small', '')
                sprite.kill() 
                self.growing_mushrooms.remove(sprite)
                StackedSprite(self, name=adult_name, pos=pos, rot=uniform(0, 360), collision=False)

        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick()

    def draw_coins(self):
        text = f"Coins: {self.coins}"
        coin_surf = self.font_coins.render(text, True, 'yellow')
        shadow_surf = self.font_coins.render(text, True, 'black')
        
        pos = (WIDTH - coin_surf.get_width() - 20, 20)
        
        self.screen.blit(shadow_surf, (pos[0] + 2, pos[1] + 2))
        self.screen.blit(coin_surf, pos)

    def draw_mushrooms(self):
        orange_count = self.inventory.get('orange_mush', 0)
        blue_count = self.inventory.get('blue_mush', 0)
        
        orange_surf = self.font_coins.render(f"Sunshrooms: {orange_count}", True, 'white')
        blue_surf = self.font_coins.render(f"Moonshrooms: {blue_count}", True, 'white')
        
        orange_shadow = self.font_coins.render(f"Sunshrooms: {orange_count}", True, 'black')
        blue_shadow = self.font_coins.render(f"Moonshrooms: {blue_count}", True, 'black')
        
        blue_pos = (20, HEIGHT - blue_surf.get_height() - 20)
        orange_pos = (20, blue_pos[1] - orange_surf.get_height() - 10)
        
        self.screen.blit(orange_shadow, (orange_pos[0] + 2, orange_pos[1] + 2))
        self.screen.blit(blue_shadow, (blue_pos[0] + 2, blue_pos[1] + 2))
        
        self.screen.blit(orange_surf, orange_pos)
        self.screen.blit(blue_surf, blue_pos)

    def draw_task(self):
        if self.tutorial_stage < len(self.tasks):
            task_text = f"TASK: {self.tasks[self.tutorial_stage]}"
            shadow = self.font_coins.render(task_text, True, 'black')
            text = self.font_coins.render(task_text, True, 'white')
            self.screen.blit(shadow, (22, 22))
            self.screen.blit(text, (20, 20))

    def draw_stars(self):
        if self.all_runes_active:
            star_surf = pg.Surface(RES, pg.SRCALPHA)
            for s in self.stars:
                glow = 210 + 45 * math.sin(pg.time.get_ticks() * s['speed'])
            
                pg.draw.circle(star_surf, (180, 230, 255, int(glow)), s['pos'], s['size'])
                pg.draw.circle(star_surf, (100, 200, 255, int(glow // 2)), s['pos'], s['size'] + 1)
            
            self.screen.blit(star_surf, (0, 0))

    def draw_interaction_msg(self):
        from scene import Scene
        if not isinstance(self.scene, Scene):
            return
        
        if self.message.active:
            return
        
        for sprite in self.entity_group:
            if hasattr(sprite, 'name') and hasattr(sprite, 'pos'):
                dist = self.player.offset.distance_to(sprite.pos)
                
                if sprite.name in ('forest_guardian', 'forest_guardian_end') and dist < 150:
                    self._render_msg("Press 'E' to Talk to Stribor")
                    break

                elif sprite.name in ('albert_wisker', 'albert_wisker_end') and dist < 150:
                    self._render_msg("Press 'E' to Talk to Albert Wisker")
                    break

                elif sprite.name in ('kosjenka', 'kosjenka_hair') and dist < 150:
                    self._render_msg("Press 'E' to Talk to Kosjenka")
                    break

                elif sprite.name in ('beetle', 'beetle_end') and dist < 150:
                    self._render_msg("Press 'E' to Talk to Lesij")
                    break

        for sprite in self.main_group:
            if hasattr(sprite, 'name') and hasattr(sprite, 'pos'):
                dist = self.player.offset.distance_to(sprite.pos)
                
                if sprite.name == 'shop' and dist < 200:
                    self._render_msg("Press 'E' to Enter Shop")
                    break

                elif sprite.name == 'bridge' and dist < 200:
                    self._render_msg("Press 'E' to Fish")
                    break

                elif sprite.name == 'mushroom1' and dist < 150:
                    self._render_msg("Press 'F' to Harvest")
                    break

                elif sprite.name == 'mushroom2' and dist < 150:
                    self._render_msg("Press 'F' to Harvest")
                    break

                elif sprite.name == 'mushroom3' and dist < 150:
                    self._render_msg("Press 'F' to Harvest")
                    break

                if 'field' in sprite.name and dist < 150:
                    grid_pos_x = int(sprite.pos.x / TILE_SIZE)
                    grid_pos_y = int(sprite.pos.y / TILE_SIZE)
                    
                    has_mushroom = False
                    is_ready = False
                    
                    for s in self.main_group:
                        if isinstance(s, StackedSprite) and 'mush' in s.name:
                            if int(s.pos.x / TILE_SIZE) == grid_pos_x and int(s.pos.y / TILE_SIZE) == grid_pos_y:
                                has_mushroom = True
                                if not s.name.endswith('_small'):
                                    is_ready = True
                                break
                    
                    if has_mushroom:
                        if is_ready:
                            self._render_msg("Press 'F' to Harvest")
                        else:
                            self._render_msg("Mushroom is growing...")
                    else:
                        self._render_msg("Press 'F' to Plant")
                    return

                elif sprite.name == 'grand_cristal' and dist < 200:
                    growing_mush = False
                    for s in self.main_group:
                        if isinstance(s, StackedSprite) and 'mush' in s.name:
                            if s.name.endswith('small'):
                                growing_mush = True
                                break
                    if growing_mush:
                        self._render_msg("Press 'E' to Start the magic")
                        break
                    else:
                        self._render_msg("There are no growing mushrooms")
                        break

                elif sprite.name == 'rune1_off' and dist < 150:
                    self._render_msg("Press 'E' to Activate the Moon rune")
                    break

                elif sprite.name == 'rune2_off' and dist < 150:
                    self._render_msg("Press 'E' to Activate the Nature rune")
                    break

                elif sprite.name == 'rune3_off' and dist < 150:
                    self._render_msg("Press 'E' to Activate the Water rune")
                    break

    def _render_msg(self, text):
        msg_surf = self.font_coins.render(text, True, 'white')
        msg_shadow = self.font_coins.render(text, True, 'black')
        pos = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT * 0.8))
        self.screen.blit(msg_shadow, (pos.x + 2, pos.y + 2))
        self.screen.blit(msg_surf, pos)

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
            if not self.message.active:
                self.draw_mushrooms()
            self.draw_task()
            self.draw_interaction_msg()
            self.draw_stars()

        pg.display.flip()

    def check_events(self):
        from scene import ShopScene, FishingScene, SimonSaysScene, Scene, ControlsScene, BookScene
        
        if isinstance(self.scene, (ShopScene, FishingScene, SimonSaysScene, ControlsScene, BookScene)):
            self.scene.update()
            return
        
        self.anim_trigger = False
        if hasattr(self.scene, 'start_rect') or hasattr(self.scene, 'resume_rect'): 
            return
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.exit_game()

            elif e.type == self.anim_event:
                self.anim_trigger = True

            elif e.type == pg.KEYDOWN:
                self.current_input.append(e.key)
                if len(self.current_input) > len(self.konami_code):
                    self.current_input.pop(0)
                if self.current_input == self.konami_code:
                    self.coins += 1000000
                    self.message.set_message("CHEAT ENABLED: + One milli!")
                    self.message.active = True
                    self.current_input = []

                if e.key == pg.K_f:
                    from scene import Scene
                    if isinstance(self.scene, Scene):
                        plant_mushroom(self, self.scene)

                if e.key == pg.K_b:
                    from scene import Scene, BookScene
                    if isinstance(self.scene, Scene):
                        if self.inventory.get('old_book'):
                            self.scene = BookScene(self, self.scene)

                elif e.key == pg.K_ESCAPE:
                    from scene import Scene
                    if isinstance(self.scene, Scene):
                        self.scene = PauseScene(self, self.scene)

                elif e.key == pg.K_e:
                    from scene import Scene, ShopScene, FishingScene
                    if isinstance(self.scene, Scene):
                        for sprite in self.entity_group:
                            if sprite.name != 'player':
                                dist = (self.player.offset - sprite.pos).length()
                                if dist < 150:
                                    if hasattr(sprite, 'message'):
                                        self.message.set_message(sprite.message)
                                        self.message.active = True
                                        break

                        for sprite in self.main_group:
                            if hasattr(sprite, 'name') and hasattr(sprite, 'pos'):
                                dist = self.player.offset.distance_to(sprite.pos)
                                if sprite.name == 'shop' and dist < 200:
                                    self.scene = ShopScene(self, self.scene)
                                    break
                                elif sprite.name == 'bridge' and dist < 200:
                                    self.scene = FishingScene(self, self.scene)
                                    break
                                elif sprite.name == 'grand_cristal' and dist < 200:
                                    growing_mush = False
                                    for s in self.main_group:
                                        from stacked_sprite import StackedSprite
                                        if isinstance(s, StackedSprite) and 'mush' in s.name:
                                            if s.name.endswith('small'):
                                                growing_mush = True
                                                break
                                    if growing_mush:
                                        self.scene = SimonSaysScene(self, self.scene)
                                        return
                                elif sprite.name in ['rune1_off', 'rune2_off', 'rune3_off'] and dist < 150:
                                    rune_data = {
                                        'rune1_off': {'key': 'key1', 'on': 'rune1_on'},
                                        'rune2_off': {'key': 'key2', 'on': 'rune2_on'},
                                        'rune3_off': {'key': 'key3', 'on': 'rune3_on'}
                                    }
    
                                    current_rune = rune_data[sprite.name]
    
                                    if self.inventory.get(current_rune['key']):
                                        from stacked_sprite import StackedSprite
                                        StackedSprite(self, name=current_rune['on'], pos=sprite.pos / TILE_SIZE, rot=180)
        
                                        sprite.kill()
        
                                        self.message.set_message(f"The forest grows brighter for a moment. Something deep beneath the roots has awakened.")
                                        self.message.active = True
                                        pg.mixer.init()
                                        try:
                                            rune_sfx = pg.mixer.Sound('assets/sfx/Rune_Activate_SFX.mp3')
                                            rune_sfx.play(loops=0, maxtime=0, fade_ms=0)
                                        except pg.error as e:
                                            print(f"Greška pri učitavanju glazbe: {e}")

                                        if hasattr(self, 'tutorial_stage'):
                                            if self.tutorial_stage in [8, 9, 10]:
                                                self.tutorial_stage += 1

                                        active_runes = 0
                                        for s in self.main_group:
                                            if hasattr(s, 'name') and s.name in ['rune1_on', 'rune2_on', 'rune3_on']:
                                                active_runes += 1

                                        if active_runes == 3:
                                            self.all_runes_active = True
                                            for s in self.main_group:
                                                if hasattr(s, 'name') and s.name == 'grand_tree':
                                                    tree_pos = s.pos / TILE_SIZE
                                                    tree_rot = s.rot
                                                    s.kill()
                                                    StackedSprite(self, name='grand_tree_grown', pos=tree_pos, rot=tree_rot)
                                                    break
                                            self.message.set_message("STRIBOR:\nAt last… The magic has returned to the forest. You gave this land hope again.")
                                            self.message.active = True
                                            pg.mixer.init()
                                            try:
                                                rune_sfx = pg.mixer.Sound('assets/sfx/Rune_Activate_SFX.mp3')
                                                rune_sfx.play(loops=0, maxtime=0, fade_ms=0)
                                            except pg.error as e:
                                                print(f"Greška pri učitavanju glazbe: {e}")
                                    else:
                                        self.message.set_message(f"Nothing happens. Perhaps a special key could awaken it.")
                                        self.message.active = True
                                    break
                
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
