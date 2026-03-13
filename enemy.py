import pygame
import random
from constants import WIDTH, GRID_SIZE, TOP_BAR_HEIGHT, HEIGHT, WHITE

pygame.init()
enemy_font = pygame.font.SysFont("SimHei", 32)

# =====================
# 敌人
# =====================
class Enemy:
    def __init__(self):
        self.grid_x = random.randint(0, WIDTH // GRID_SIZE - 1)
        self.x = self.grid_x * GRID_SIZE
        self.y = TOP_BAR_HEIGHT
        self.size = GRID_SIZE
        self.speed = 2

        self.hp = random.randint(1, 5)   # ★ 1e：血量

    def hit(self):
        self.hp -= 1

    def update(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        # 敌人圆
        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + GRID_SIZE // 2, int(self.y + GRID_SIZE // 2)),
            GRID_SIZE // 2 - 4
        )

        # ★ 1e：血量数字
        text = enemy_font.render(str(self.hp), True, (0, 0, 0))
        rect = text.get_rect(center=(self.x + GRID_SIZE // 2,
                                     self.y + GRID_SIZE // 2))
        screen.blit(text, rect)

class SnakeEnemy:
    def __init__(self):
        # 使用网格坐标跟踪行
        self.grid_y = 0                  # 记录当前行号
        self.x = 0 * GRID_SIZE
        self.y = TOP_BAR_HEIGHT
        self.size = GRID_SIZE
        self.speed = 2

        self.hp = random.randint(1, 5)

        # 初始状态向右（第0行是偶数行）
        self.state = "right"      # "right" / "left" / "down"

    def hit(self):
        self.hp -= 1

    def update(self):
        # 根据当前状态移动
        if self.state == "right":
            self.x += self.speed
            if self.x >= WIDTH - GRID_SIZE:
                self.x = WIDTH - GRID_SIZE
                self.state = "down"

        elif self.state == "left":
            self.x -= self.speed
            if self.x <= 0:
                self.x = 0
                self.state = "down"

        elif self.state == "down":
            self.y += self.speed
            if self.y % GRID_SIZE == 0:
                self.grid_y += 1
                # 每两行改变一次方向（隔一行）
                # 0, 4, 8...行向右，2, 6, 10...行向左
                if self.grid_y % 4 == 0:
                    self.state = "right"
                elif self.grid_y % 4 == 2:
                    self.state = "left"


    def is_off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + GRID_SIZE // 2, int(self.y + GRID_SIZE // 2)),
            GRID_SIZE // 2 - 4
        )
        text = enemy_font.render(str(self.hp), True, (0, 0, 0))
        rect = text.get_rect(center=(self.x + GRID_SIZE // 2,
                                     self.y + GRID_SIZE // 2))
        screen.blit(text, rect)