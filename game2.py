import pygame
import time
from constants import *
from player import Player
from enemy import SnakeEnemy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game - 1d")
clock = pygame.time.Clock()
font = pygame.font.SysFont("SimHei", 22)

# =====================
# 绘制网格
# =====================
def draw_grid(screen):
    # 只绘制横向网格线
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y)
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
            enemies.append(SnakeEnemy())
            enemy_timer = 0

        # 更新敌人
        for enemy in enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                enemies.remove(enemy)

        # ★ 1e：子弹 × 敌人（减血）
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.get_rect().collidepoint(bullet.x, bullet.y):
                    bullets.remove(bullet)
                    enemy.hit()
                    if enemy.hp <= 0:
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