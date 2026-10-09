"""player.py - The Player class (the basket the user controls)."""
import pygame

from settings import WIDTH, HEIGHT, PLAYER_SIZE, PLAYER_MAX_SPEED, PLAYER_ACCEL, PLAYER_BOTTOM_MARGIN


class Player(pygame.sprite.Sprite):
    """The basket. Uses acceleration so movement feels smooth, not jerky."""

    def __init__(self, assets):
        super().__init__()
        self.image = assets.image("basket.png", PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.x = WIDTH / 2.0
        self.vx = 0.0
        self.rect.midbottom = (round(self.x), HEIGHT - PLAYER_BOTTOM_MARGIN)

    @property
    def catch_rect(self):
        """Only the opening of the basket catches items (more fair than the full sprite)."""
        return pygame.Rect(self.rect.left + 12, self.rect.top, self.rect.width - 24, 28)

    def update(self, dt, keys):
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1
        target = direction * PLAYER_MAX_SPEED
        # ease the velocity towards the target speed (smooth acceleration / braking)
        self.vx += (target - self.vx) * min(1.0, PLAYER_ACCEL * dt)
        self.x += self.vx * dt
        half = self.rect.width / 2
        if self.x < half:
            self.x, self.vx = half, 0
        elif self.x > WIDTH - half:
            self.x, self.vx = WIDTH - half, 0
        self.rect.centerx = round(self.x)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
