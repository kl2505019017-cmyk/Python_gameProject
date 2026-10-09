"""level.py - Level definitions: each level is harder than the last."""
import random

from item import Apple, Orange, Banana, Bomb, HeartPowerUp, GoldenStar


class Level:
    def __init__(self, number, spawn_interval, start_speed, weights):
        self.number = number
        self.spawn_interval = spawn_interval   # seconds between spawns
        self.start_speed = start_speed         # initial downward speed (px/s)
        self.weights = weights                 # {ItemClass: chance weight}

    def random_item_class(self):
        classes = list(self.weights.keys())
        return random.choices(classes, weights=list(self.weights.values()), k=1)[0]


# 4 levels x 15 seconds = 60 seconds. Faster spawns, faster items, more bombs.
LEVELS = [
    Level(1, 1.10, 60,  {Apple: 30, Orange: 30, Banana: 20, Bomb: 12, HeartPowerUp: 4, GoldenStar: 3}),
    Level(2, 0.90, 100, {Apple: 26, Orange: 26, Banana: 20, Bomb: 20, HeartPowerUp: 4, GoldenStar: 3}),
    Level(3, 0.72, 150, {Apple: 22, Orange: 22, Banana: 20, Bomb: 28, HeartPowerUp: 4, GoldenStar: 3}),
    Level(4, 0.58, 200, {Apple: 20, Orange: 20, Banana: 20, Bomb: 34, HeartPowerUp: 4, GoldenStar: 3}),
]
