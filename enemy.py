import pygame
import random
from constants import WIDTH, GRID_SIZE, TOP_BAR_HEIGHT, HEIGHT, WHITE

# =====================
# 敌人（★ 1d 新增）
# =====================
class Enemy:
    def __init__(self):
        self.grid_x = random.randint(0, WIDTH // GRID_SIZE - 1)
        self.x = self.grid_x * GRID_SIZE
        self.y = TOP_BAR_HEIGHT
        self.size = GRID_SIZE
        self.speed = 2

    def update(self):
        self.y += self.speed

    def is_off_screen(self):
        if self.y > HEIGHT:
            return True 
        else:
            return False
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + GRID_SIZE // 2, int(self.y + GRID_SIZE // 2)),
            GRID_SIZE // 2 - 4
        )