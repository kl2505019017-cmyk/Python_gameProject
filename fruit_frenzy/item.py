"""item.py - Falling items. Item is the base class; each subclass changes the behaviour
(polymorphism): fruits give points, bombs cost a life, hearts give a life back."""
import random
import pygame

from settings import ITEM_SIZE, GRAVITY, MAX_FALL_SPEED


class Item(pygame.sprite.Sprite):
    """Base class for everything that falls. Subclasses override the behaviour."""

    image_name = None
    is_fruit = False

    def __init__(self, assets, x, start_speed):
        super().__init__()
        self.image = assets.image(self.image_name, ITEM_SIZE)
        self.rect = self.image.get_rect(midbottom=(x, 0))
        self.pos_y = float(self.rect.y)
        self.vy = start_speed + random.uniform(0, 30)

    def update(self, dt):
        # gravity: velocity grows every frame, position follows velocity
        self.vy = min(self.vy + GRAVITY * dt, MAX_FALL_SPEED)
        self.pos_y += self.vy * dt
        self.rect.y = round(self.pos_y)

    def on_caught(self, game):
        raise NotImplementedError

    def on_missed(self, game):
        pass


class Fruit(Item):
    is_fruit = True
    points = 10

    def on_caught(self, game):
        game.add_score(self.points, self.rect.center)
        game.assets.sound("catch.wav").play()

    def on_missed(self, game):
        game.lose_life(self.rect.midbottom)
        game.assets.sound("miss.wav").play()


class Apple(Fruit):
    image_name = "apple.png"
    points = 10


class Orange(Fruit):
    image_name = "orange.png"
    points = 10


class Banana(Fruit):
    image_name = "banana.png"
    points = 15


class Bomb(Item):
    image_name = "bomb.png"

    def on_caught(self, game):
        game.lose_life(self.rect.center)
        game.assets.sound("bomb.wav").play()


class HeartPowerUp(Item):
    image_name = "heart.png"

    def on_caught(self, game):
        game.add_life(self.rect.center)
        game.assets.sound("powerup.wav").play()


class GoldenStar(Item):
    """Rare bonus item: worth a lot of points but appears only occasionally."""
    image_name = "star.png"

    def on_caught(self, game):
        game.add_score(30, self.rect.center)
        game.assets.sound("powerup.wav").play()

