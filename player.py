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


# =====================
# 玩家（倒 T 形 / Inverted T）
# 底部 3 格 + 上面中间 1 格
# 并且可以同时发射 3 颗子弹
# =====================
class AdvancedPlayer:
    def __init__(self):
        # grid_x 表示“底部最左边那个方块”的列索引
        # 这样底部 3 格就是：
        # (grid_x, grid_y)
        # (grid_x + 1, grid_y)
        # (grid_x + 2, grid_y)
        #
        # 上面伸出去的头是：
        # (grid_x + 1, grid_y - 1)

        self.grid_x = WIDTH // GRID_SIZE // 2 - 1   # 让整体大致居中
        self.grid_y = (HEIGHT - GRID_SIZE) // GRID_SIZE  # 底部一行

        self.counter = 0        # 计数器（帧）
        self.shoot_space = 10   # 发射间隔（帧）

    def move(self, direction):
        """
        玩家左右移动
        direction:
            -1 -> 向左
             1 -> 向右
        """
        self.grid_x += direction

        # 因为底部占 3 格，所以最右不能超出屏幕
        max_x = WIDTH // GRID_SIZE - 3

        if self.grid_x < 0:
            self.grid_x = 0
        if self.grid_x > max_x:
            self.grid_x = max_x

    def shoot(self, bullets):
        """
        根据 blocks（炮口位置）发射子弹, 3 个炮口 每个 block 发射一颗
        1. 左侧炮口：底部左格的中点
        2. 中间炮口：上方中间“头”的中点
        3. 右侧炮口：底部右格的中点
        """
        if self.counter % self.shoot_space == 0:
            # 三个炮口（从 blocks 直接取）
            blocks = [ 
                (self.grid_x, self.grid_y),         # 左
                (self.grid_x + 2, self.grid_y),     # 右
                (self.grid_x + 1, self.grid_y - 1)  # 中间上方
            ]

            for gx, gy in blocks:
                # 转换为像素坐标（子弹从方块中心发射）
                x = gx * GRID_SIZE + GRID_SIZE // 2
                y = gy * GRID_SIZE

                bullets.append(Bullet(x, y))

        self.counter += 1

    def draw(self, screen):
        """
        绘制倒 T 形玩家
        形状如下：

            [ ][X][ ]
            [X][X][X]

        实际只画蓝色方块：
              中间上方 1 格
              底部一排 3 格
        """
        blocks = [
            (self.grid_x, self.grid_y),         # 底部左
            (self.grid_x + 1, self.grid_y),     # 底部中
            (self.grid_x + 2, self.grid_y),     # 底部右
            (self.grid_x + 1, self.grid_y - 1)  # 上方中间“头”
        ]

        for gx, gy in blocks:
            x = gx * GRID_SIZE
            y = gy * GRID_SIZE
            pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))