import pygame
import random
import time

WIDTH, HEIGHT = 400, 700
GRID_SIZE = 40
TOP_BAR_HEIGHT = 40
FPS = 60

BG_COLOR = (40, 40, 40)      # 深灰色背景
GRID_COLOR = (100, 100, 100) # 网格线颜色
BLUE = (50, 150, 255)
RED = (255, 60, 50)
WHITE = (230, 230, 230)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game - 1d")
clock = pygame.time.Clock()
font = pygame.font.SysFont("SimHei", 22)

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

    
# =====================
# 玩家（只负责位置）
# =====================
class Player:
    def __init__(self):
        self.grid_x = WIDTH //GRID_SIZE // 2 # 位于中间列
        self.grid_y = (HEIGHT - GRID_SIZE) // GRID_SIZE # 底部一行
        self.counter = 0 # 计数器（帧）
        self.shoot_space = 20 # 发射间隔（帧）
    
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
# =====================
# 绘制网格
# =====================
def draw_grid(screen):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, HEIGHT)
        )

# =====================
# 顶部信息栏（★ 1d 新增）
# =====================
def draw_top_bar(screen, score):
    pygame.draw.rect(screen, (25, 25, 25), (0, 0, WIDTH, TOP_BAR_HEIGHT))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 8))

# =====================
# 主循环
# =====================
def main():
    player = Player()
    bullets = []
    enemies = []
    score = 0
    enemy_timer = 0

    running = True

    last_move = time.time()
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            cur_time = time.time()
            if cur_time - last_move >= 0.1: # 每 0.1 秒允许一次移动
                player.move(-1)
                last_move = cur_time


        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            cur_time = time.time()
            if cur_time - last_move >= 0.1: # 每 0.1 秒允许一次移动
                player.move(1)
                last_move = cur_time

        player.shoot(bullets)

        # 更新子弹
        for bullet in bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                bullets.remove(bullet)

        # ★ 生成敌人
        enemy_timer += 1
        if enemy_timer >= 60:
            enemies.append(Enemy())
            enemy_timer = 0

        # 更新敌人
        for enemy in enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                enemies.remove(enemy)

        # ★ 碰撞检测
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.get_rect().collidepoint(bullet.x, bullet.y):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # ===== 绘制 =====s
        screen.fill(BG_COLOR)
        draw_top_bar(screen, score)
        draw_grid(screen)

        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()