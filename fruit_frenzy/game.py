"""game.py - The Game class: state machine, game loop, rules, menus and drawing."""
import random
import sys
import pygame

from settings import *
from utils import AssetManager, FloatingText
from player import Player
from language import Translator
from level import LEVELS

# Game states
MENU, INSTRUCTIONS, PLAYING, PAUSED, GAME_OVER = range(5)
MENU_OPTIONS = ["start", "instructions", "language", "exit"]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.t = Translator("en")

        self.font_big = pygame.font.SysFont("arial", 64, bold=True)
        self.font_med = pygame.font.SysFont("arial", 32, bold=True)
        self.font = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 18)

        self.background = self.assets.background("background.png", (WIDTH, HEIGHT))
        self.heart_icon = self.assets.image("heart.png", (30, 30))

        self.player = Player(self.assets)
        self.items = pygame.sprite.Group()
        self.effects = []

        self.high_score = self.load_high_score()
        self.state = MENU
        self.menu_index = 0
        self.running = True
        self.reset_round()

    # ------------------------------------------------------------------ setup
    def reset_round(self):
        self.score = 0
        self.lives = START_LIVES
        self.combo = 0
        self.time_left = float(GAME_DURATION)
        self.spawn_timer = 0.0
        self.level_index = 0
        self.banner_timer = 0.0
        self.won = False
        self.new_record = False
        self.items.empty()
        self.effects.clear()
        self.player.reset()

    def start_game(self):
        self.reset_round()
        self.state = PLAYING
        self.banner_timer = 1.5

    # ------------------------------------------------------------ high score
    def load_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            return 0

    def save_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.high_score))
        except OSError:
            pass

    # ------------------------------------------------------------ game rules
    @property
    def level(self):
        return LEVELS[self.level_index]

    @property
    def multiplier(self):
        return min(3, 1 + self.combo // 5)

    def add_score(self, points, pos):
        gained = points * self.multiplier
        self.score += gained
        self.combo += 1
        self.effects.append(FloatingText(f"+{gained}", pos, self.font_med, YELLOW))

    def lose_life(self, pos):
        self.lives -= 1
        self.combo = 0
        self.effects.append(FloatingText("-1", pos, self.font_med, RED))

    def add_life(self, pos):
        if self.lives < MAX_LIVES:
            self.lives += 1
        self.effects.append(FloatingText("+1", pos, self.font_med, GREEN))

    def spawn_item(self):
        cls = self.level.random_item_class()
        half = ITEM_SIZE[0] // 2
        x = random.randint(half + 10, WIDTH - half - 10)
        self.items.add(cls(self.assets, x, self.level.start_speed))

    def end_round(self, won):
        self.won = won
        self.state = GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_record = True
            self.save_high_score()
        self.assets.sound("win.wav" if won else "lose.wav").play()

    # ----------------------------------------------------------------- events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if self.state == MENU:
                    self.menu_keys(key)
                elif self.state == INSTRUCTIONS:
                    self.state = MENU
                elif self.state == PLAYING:
                    if key == pygame.K_p:
                        self.state = PAUSED
                    elif key == pygame.K_r:
                        self.start_game()
                    elif key == pygame.K_ESCAPE:
                        self.state = MENU
                elif self.state == PAUSED:
                    if key == pygame.K_p:
                        self.state = PLAYING
                    elif key == pygame.K_r:
                        self.start_game()
                    elif key == pygame.K_ESCAPE:
                        self.state = MENU
                elif self.state == GAME_OVER:
                    if key in (pygame.K_r, pygame.K_RETURN):
                        self.start_game()
                    elif key == pygame.K_ESCAPE:
                        self.state = MENU

    def menu_keys(self, key):
        if key == pygame.K_UP:
            self.menu_index = (self.menu_index - 1) % len(MENU_OPTIONS)
        elif key == pygame.K_DOWN:
            self.menu_index = (self.menu_index + 1) % len(MENU_OPTIONS)
        elif key == pygame.K_l:
            self.t.toggle()
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            choice = MENU_OPTIONS[self.menu_index]
            if choice == "start":
                self.start_game()
            elif choice == "instructions":
                self.state = INSTRUCTIONS
            elif choice == "language":
                self.t.toggle()
            elif choice == "exit":
                self.running = False

    # ----------------------------------------------------------------- update
    def update(self, dt):
        for fx in self.effects:
            fx.update(dt)
        self.effects = [fx for fx in self.effects if fx.alive]

        if self.state != PLAYING:
            return

        self.player.update(dt, pygame.key.get_pressed())

        # timer and level progression
        self.time_left -= dt
        elapsed = GAME_DURATION - self.time_left
        new_index = min(len(LEVELS) - 1, int(elapsed // LEVEL_LENGTH))
        if new_index != self.level_index:
            self.level_index = new_index
            self.banner_timer = 1.8
        self.banner_timer = max(0.0, self.banner_timer - dt)

        # spawning
        self.spawn_timer += dt
        if self.spawn_timer >= self.level.spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_item()

        # move items, then check collisions / misses
        self.items.update(dt)
        catcher = self.player.catch_rect
        for item in list(self.items):
            if item.rect.colliderect(catcher) and item.rect.centery < catcher.bottom:
                item.on_caught(self)
                item.kill()
            elif item.rect.top > HEIGHT:
                item.on_missed(self)
                item.kill()

        # win / lose conditions
        if self.lives <= 0:
            self.lives = 0
            self.end_round(False)
        elif self.time_left <= 0:
            self.time_left = 0
            self.end_round(True)

    # ------------------------------------------------------------------- draw
    def draw_text(self, text, font, colour, pos, center=True):
        surf = font.render(text, True, colour)
        rect = surf.get_rect(center=pos) if center else surf.get_rect(topleft=pos)
        self.screen.blit(surf, rect)
        return rect

    def draw_overlay(self, alpha=150):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((10, 15, 30, alpha))
        self.screen.blit(shade, (0, 0))

    def draw_hud(self):
        bar = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
        bar.fill((15, 25, 45, 170))
        self.screen.blit(bar, (0, 0))
        self.draw_text(f"{self.t('score')}: {self.score}", self.font, WHITE, (12, 10), False)
        self.draw_text(f"{self.t('best')}: {self.high_score}", self.font_small, YELLOW, (190, 14), False)
        self.draw_text(f"{self.t('time')}: {max(0, int(self.time_left + 0.99))}", self.font, WHITE, (350, 10), False)
        self.draw_text(f"{self.t('level')}: {self.level.number}", self.font, WHITE, (470, 10), False)
        if self.multiplier > 1:
            self.draw_text(f"{self.t('combo')} x{self.multiplier}", self.font, YELLOW, (590, 10), False)
        for i in range(self.lives):
            self.screen.blit(self.heart_icon, (WIDTH - 36 * (i + 1) - 4, 7))

    def draw_world(self):
        self.screen.blit(self.background, (0, 0))
        self.items.draw(self.screen)
        self.player.draw(self.screen)
        for fx in self.effects:
            fx.draw(self.screen)
        self.draw_hud()
        if self.state == PLAYING and self.banner_timer > 0:
            self.draw_text(self.t("level_up", n=self.level.number), self.font_big, WHITE, (WIDTH // 2, 200))

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_overlay(90)
        self.draw_text(self.t("title"), self.font_big, YELLOW, (WIDTH // 2, 110))
        self.draw_text(self.t("subtitle"), self.font, WHITE, (WIDTH // 2, 170))
        for i, key in enumerate(MENU_OPTIONS):
            selected = i == self.menu_index
            colour = YELLOW if selected else WHITE
            label = ("> " + self.t(key) + " <") if selected else self.t(key)
            self.draw_text(label, self.font_med, colour, (WIDTH // 2, 255 + i * 55))
        self.draw_text(self.t("menu_hint"), self.font_small, WHITE, (WIDTH // 2, HEIGHT - 30))

    def draw_instructions(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_overlay(170)
        self.draw_text(self.t("how_title"), self.font_med, YELLOW, (WIDTH // 2, 55))
        y = 110
        for line in self.t("how_lines"):
            self.draw_text(line, self.font_small, WHITE, (WIDTH // 2, y))
            y += 32
        # item legend with icons
        legend = [
            ("apple.png", f"+10 {self.t('points')}"),
            ("orange.png", f"+10 {self.t('points')}"),
            ("banana.png", f"+15 {self.t('points')}"),
            ("star.png", f"+30 {self.t('points')}"),
            ("heart.png", f"+1 {self.t('life')}"),
            ("bomb.png", self.t("bomb")),
        ]
        x = 60
        for name, text in legend:
            self.screen.blit(self.assets.image(name, ITEM_SIZE), (x, 380))
            self.draw_text(text, self.font_small, WHITE, (x + 26, 450))
            x += 125
        self.draw_text(self.t("back_hint"), self.font_small, YELLOW, (WIDTH // 2, HEIGHT - 40))

    def draw_pause(self):
        self.draw_world()
        self.draw_overlay(150)
        self.draw_text(self.t("paused"), self.font_big, WHITE, (WIDTH // 2, 240))
        self.draw_text(self.t("paused_hint"), self.font, WHITE, (WIDTH // 2, 320))

    def draw_game_over(self):
        self.draw_world()
        self.draw_overlay(170)
        title = self.t("win") if self.won else self.t("lose")
        self.draw_text(title, self.font_big, GREEN if self.won else RED, (WIDTH // 2, 190))
        self.draw_text(f"{self.t('final_score')}: {self.score}", self.font_med, WHITE, (WIDTH // 2, 280))
        self.draw_text(f"{self.t('best')}: {self.high_score}", self.font, YELLOW, (WIDTH // 2, 325))
        if self.new_record:
            self.draw_text(self.t("new_best"), self.font_med, YELLOW, (WIDTH // 2, 375))
        self.draw_text(self.t("over_hint"), self.font, WHITE, (WIDTH // 2, 450))

    def draw(self):
        if self.state == MENU:
            self.draw_menu()
        elif self.state == INSTRUCTIONS:
            self.draw_instructions()
        elif self.state == PLAYING:
            self.draw_world()
        elif self.state == PAUSED:
            self.draw_pause()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        pygame.display.flip()

    # -------------------------------------------------------------- main loop
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)  # cap dt so lag spikes do not teleport items
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()
