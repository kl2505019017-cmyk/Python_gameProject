"""utils.py - Helper code: safe asset loading (with shape fallbacks) and floating text."""
import os
import pygame

from settings import IMAGE_DIR, SOUND_DIR, WHITE


def make_fallback(name, size):
    """Draw a simple picture with Pygame shapes when the image file is missing,
    so the game still runs with no image assets at all."""
    w, h = size
    surf = pygame.Surface(size, pygame.SRCALPHA)
    c = (w // 2, h // 2)
    r = min(w, h) // 2 - 2
    if name == "apple.png":
        pygame.draw.circle(surf, (215, 45, 45), c, r)
        pygame.draw.ellipse(surf, (70, 170, 70), (w // 2, 1, w // 3, h // 5))
    elif name == "orange.png":
        pygame.draw.circle(surf, (250, 150, 30), c, r)
        pygame.draw.ellipse(surf, (70, 170, 70), (w // 2 - 4, 1, w // 3, h // 6))
    elif name == "banana.png":
        pygame.draw.ellipse(surf, (250, 220, 60), (2, h // 4, w - 4, h // 2))
        pygame.draw.ellipse(surf, (0, 0, 0, 0), (w // 5, h // 6, w - 4, h // 2))
    elif name == "bomb.png":
        pygame.draw.circle(surf, (40, 40, 48), (c[0], c[1] + 4), r - 4)
        pygame.draw.line(surf, (200, 150, 60), (c[0], 8), (c[0] + 8, 1), 3)
        pygame.draw.circle(surf, (255, 210, 50), (c[0] + 9, 3), 3)
    elif name == "heart.png":
        pygame.draw.circle(surf, (235, 50, 90), (w // 3, h // 3), w // 4)
        pygame.draw.circle(surf, (235, 50, 90), (2 * w // 3, h // 3), w // 4)
        pygame.draw.polygon(surf, (235, 50, 90), [(w // 12, h // 2), (11 * w // 12, h // 2), (c[0], h - 2)])
    elif name == "star.png":
        pts = []
        for i in range(10):
            ang = -1.5708 + i * 0.62832
            rad = r if i % 2 == 0 else r * 0.45
            pts.append((c[0] + rad * pygame.math.Vector2(1, 0).rotate_rad(ang).x,
                        c[1] + rad * pygame.math.Vector2(1, 0).rotate_rad(ang).y))
        pygame.draw.polygon(surf, (255, 205, 40), pts)
    elif name == "basket.png":
        pygame.draw.polygon(surf, (185, 125, 55), [(2, h // 3), (w - 2, h // 3), (w - 14, h - 2), (14, h - 2)])
        pygame.draw.rect(surf, (150, 95, 40), (0, h // 4, w, h // 6), border_radius=5)
        pygame.draw.arc(surf, (120, 80, 35), (w // 5, 0, 3 * w // 5, h), 0, 3.1416, 4)
    else:  # unknown name: visible magenta box
        surf.fill((255, 0, 255))
    return surf


def make_fallback_background(size):
    """Vertical sky gradient + grass strip, drawn with shapes."""
    w, h = size
    surf = pygame.Surface(size)
    for y in range(h):
        t = y / h
        pygame.draw.line(surf, (int(110 + 100 * t), int(185 + 50 * t), 245), (0, y), (w, y))
    pygame.draw.rect(surf, (75, 150, 80), (0, h - 60, w, 60))
    return surf


class _SilentSound:
    """Stand-in used when a sound file or the audio device is unavailable."""

    def play(self):
        pass


class AssetManager:
    """Loads images/sounds once (cached). Never crashes if a file is missing."""

    def __init__(self):
        self._images = {}
        self._sounds = {}
        self.audio_ok = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            self.audio_ok = False

    def image(self, name, size):
        key = (name, size)
        if key not in self._images:
            try:
                img = pygame.image.load(os.path.join(IMAGE_DIR, name)).convert_alpha()
                img = pygame.transform.smoothscale(img, size)
            except (pygame.error, FileNotFoundError):
                img = make_fallback(name, size)
            self._images[key] = img
        return self._images[key]

    def background(self, name, size):
        key = (name, size, "bg")
        if key not in self._images:
            try:
                img = pygame.image.load(os.path.join(IMAGE_DIR, name)).convert()
                img = pygame.transform.smoothscale(img, size)
            except (pygame.error, FileNotFoundError):
                img = make_fallback_background(size)
            self._images[key] = img
        return self._images[key]

    def sound(self, name, volume=0.6):
        if name not in self._sounds:
            snd = _SilentSound()
            if self.audio_ok:
                try:
                    snd = pygame.mixer.Sound(os.path.join(SOUND_DIR, name))
                    snd.set_volume(volume)
                except (pygame.error, FileNotFoundError):
                    pass
            self._sounds[name] = snd
        return self._sounds[name]


class FloatingText:
    """Short-lived text that rises and fades (e.g. '+10', '-1 life')."""

    def __init__(self, text, pos, font, colour=WHITE, duration=0.9):
        self.surf = font.render(text, True, colour)
        self.x, self.y = pos
        self.duration = duration
        self.age = 0.0

    @property
    def alive(self):
        return self.age < self.duration

    def update(self, dt):
        self.age += dt
        self.y -= 45 * dt

    def draw(self, surface):
        alpha = max(0, int(255 * (1 - self.age / self.duration)))
        self.surf.set_alpha(alpha)
        surface.blit(self.surf, self.surf.get_rect(center=(round(self.x), round(self.y))))
