import pygame
from constants import RED

# =====================
# 子弹
# =====================
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = -8

    def update(self):
        self.y += self.speed

    def is_off_screen(self):
        if self.y <0:
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)
