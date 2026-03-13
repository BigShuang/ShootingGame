import pygame
import time
from constants import *
from player import Player
from enemy import SnakeEnemy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game - v2")
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
    enemy_num = 0

    running = True

    last_move = time.time()
    dead_enemy_indexes = [] # 记录死亡的敌人索引, 用于控制移动

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

        # ★ 生成敌人（链状，最多 50 个）
        
        if enemy_num == 0:
            new_enemy = SnakeEnemy(enemy_num)
            enemies.append(new_enemy)
            enemy_num += 1
        elif enemy_num < 50:
            tail = enemies[-1]
            if tail.grid_y == 0 and tail.x > 0:
                new_enemy = SnakeEnemy(enemy_num)
                new_enemy.x = tail.x - GRID_SIZE + 4
                enemies.append(new_enemy)
                enemy_num+=1


        # 更新敌人：每个独立沿着路径，但状态同步以一起移动
        for enemy in enemies[:]:
            if len(dead_enemy_indexes) == 0:
                enemy.update()
            elif enemy.index > dead_enemy_indexes[-1]:  #  只有索引在最后一个死亡敌人之后的敌人才移动
                enemy.update()
                
            if enemy.is_off_screen():
                enemies.remove(enemy)
        
        # 检查死亡敌人的前后单元是否连接在了一起
        if len(dead_enemy_indexes) > 0:
            last_dead_index = dead_enemy_indexes[-1]
            # 寻找 last_dead_index 前后存在的敌人
            fronts = [e for e in enemies if e.index < last_dead_index]
            backs = [e for e in enemies if e.index > last_dead_index]
            if len(fronts) > 0 and len(backs) > 0:
                front = fronts[-1]  # 最后一个前面敌人
                back = backs[0]     # 第一个后面敌人
                # 如果它们在同一行且相距一个格子，则认为它们连接在一起了
                if abs(front.x - back.x) + abs(front.y - back.y) <=  GRID_SIZE - 3:
                    dead_enemy_indexes.pop()  # 移除最后一个死亡敌人索引，认为它已经连接好了
            else:
                # 如果没有前面或后面敌人了，也认为连接好了
                dead_enemy_indexes.pop()

        # ★ 1e：子弹 × 敌人（减血）
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.get_rect().collidepoint(bullet.x, bullet.y):
                    bullets.remove(bullet)
                    enemy.hit()
                    if enemy.hp <= 0:
                        dead_enemy_indexes.append(enemy.index) # 记录死亡敌人索引
                        enemies.remove(enemy)
                        score += 1
                    break

        # 保持索引有序, 从小到大
        dead_enemy_indexes.sort() 

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