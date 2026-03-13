import pygame
from constants import WIDTH, HEIGHT, GRID_SIZE, BLUE
from bullet import Bullet

# =====================
# 玩家（只负责位置）
# =====================
class Player:
    def __init__(self):
        self.grid_x = WIDTH //GRID_SIZE // 2 # 位于中间列
        self.grid_y = (HEIGHT - GRID_SIZE) // GRID_SIZE # 底部一行
        self.counter = 0 # 计数器（帧）
        self.shoot_space = 10 # 发射间隔（帧）
    
    def move(self, direction):
        self.grid_x += direction
        max_x = WIDTH // GRID_SIZE - 1
        if self.grid_x < 0:
            self.grid_x = 0
        if self.grid_x > max_x:
            self.grid_x = max_x

    def shoot(self, bullets):
        """
        创建一颗子弹，加入 bullets 列表
        """
        if self.counter % self.shoot_space == 0:
            x = self.grid_x * GRID_SIZE + GRID_SIZE // 2
            y = self.grid_y * GRID_SIZE
            b = Bullet(x, y)
            bullets.append(b)

        self.counter += 1

    def draw(self, screen):
        x = self.grid_x * GRID_SIZE
        y = self.grid_y * GRID_SIZE
        pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))
