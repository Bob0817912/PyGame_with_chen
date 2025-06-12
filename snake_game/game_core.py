"""
贪吃蛇游戏核心逻辑
"""

import pygame
import random
import math
import time
import json
import os
from typing import List, Tuple, Dict, Optional

from .enums import Direction, GameMode, PowerUpType, PowerUp
from .particle_system import ParticleEffect
from .snake_skin import SnakeSkin
from .ai_snake import AISnake
from .sound_manager import SoundManager
from .achievement_system import AchievementSystem

# 初始化pygame
pygame.init()

class UltimateSnakeGame:
    """无敌蛇王主游戏类"""
    
    def __init__(self):
        # 基础设置
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 800
        self.GRID_SIZE = 30
        self.GRID_WIDTH = self.WINDOW_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.WINDOW_HEIGHT // self.GRID_SIZE
        
        # 初始化显示
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 无敌蛇王 - Ultimate Snake Game")
        
        # 游戏组件
        self.particle_system = ParticleEffect()
        self.snake_skin = SnakeSkin()
        self.sound_manager = SoundManager()
        self.achievements = AchievementSystem()
        
        # 字体 - 使用支持中文的字体
        try:
            font_path = "C:\\Windows\\Fonts\\simhei.ttf"  # 使用黑体
            self.font_large = pygame.font.Font(font_path, 48)
            self.font_medium = pygame.font.Font(font_path, 36)
            self.font_small = pygame.font.Font(font_path, 24)
        except:
            # 如果加载失败，退回到默认字体
            print("无法加载中文字体，使用默认字体")
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        
        # 墙壁 (需要在reset_game之前初始化)
        self.walls = []
        
        # 游戏状态
        self.game_mode = GameMode.CLASSIC
        self.game_state = 'menu'  # menu, playing, paused, game_over
        self.reset_game()
        
        # 菜单系统
        self.menu_options = list(GameMode)
        self.menu_selected = 0
        
        # 统计数据
        self.stats = {
            'games_played': 0,
            'total_food_eaten': 0,
            'highest_score': 0,
            'total_playtime': 0
        }
        self.load_stats()
    
    def reset_game(self):
        """重置游戏"""
        # 蛇的初始化
        center_x = self.GRID_WIDTH // 2
        center_y = self.GRID_HEIGHT // 2
        self.snake_body = [(center_x, center_y)]
        self.snake_direction = Direction.RIGHT
        self.grow_pending = 0
        
        # AI蛇（对战模式）
        self.ai_snake = AISnake((center_x, center_y + 5), self.GRID_HEIGHT)
        
        # 食物和道具
        self.food_pos = self.generate_food()
        self.powerups = []
        self.active_effects = {}
        
        # 游戏参数
        self.score = 0
        self.speed = 5
        self.base_speed = 5
        self.level = 1
        self.food_eaten = 0
        
        # 时间管理
        self.game_time = 0
        self.last_move_time = 0
        self.last_powerup_spawn = 0
        
        # 特殊效果
        self.screen_shake = 0
        self.invincible = False
        self.frozen = False
        
        # 迷宫模式的墙壁
        self.walls = []
        if self.game_mode == GameMode.MAZE:
            self.generate_maze()
    
    def generate_food(self) -> Tuple[int, int]:
        """生成食物位置"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake_body and (x, y) not in self.walls:
                return (x, y)
    
    def generate_maze(self):
        """生成迷宫"""
        self.walls = []
        
        # 简单的迷宫生成：随机放置墙壁
        wall_count = (self.GRID_WIDTH * self.GRID_HEIGHT) // 8
        
        for _ in range(wall_count):
            x = random.randint(1, self.GRID_WIDTH - 2)
            y = random.randint(1, self.GRID_HEIGHT - 2)
            
            # 确保不在蛇的位置
            if (x, y) not in self.snake_body:
                self.walls.append((x, y))
    
    def spawn_powerup(self):
        """生成道具"""
        if len(self.powerups) >= 3:  # 最多3个道具
            return
        
        # 随机选择道具类型
        powerup_type = random.choice(list(PowerUpType))
        
        # 道具颜色
        colors = {
            PowerUpType.SPEED_BOOST: (255, 100, 100),
            PowerUpType.SLOW_MOTION: (100, 100, 255),
            PowerUpType.INVINCIBLE: (255, 255, 0),
            PowerUpType.DOUBLE_SCORE: (255, 165, 0),
            PowerUpType.SHRINK: (255, 0, 255),
            PowerUpType.TELEPORT: (0, 255, 255),
            PowerUpType.FREEZE: (200, 200, 255)
        }
        
        # 生成位置
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if ((x, y) not in self.snake_body and 
                (x, y) != self.food_pos and 
                (x, y) not in self.walls):
                
                powerup = PowerUp(
                    pos=(x, y),
                    type=powerup_type,
                    color=colors[powerup_type],
                    lifetime=15.0  # 15秒后消失
                )
                self.powerups.append(powerup)
                break

    def apply_powerup(self, powerup: PowerUp):
        """应用道具效果"""
        effect_type = powerup.type
        duration = powerup.effect_duration

        self.active_effects[effect_type] = time.time() + duration
        self.achievements.used_powerups.add(effect_type)

        if effect_type == PowerUpType.SPEED_BOOST:
            self.speed = min(30, self.base_speed * 2)
        elif effect_type == PowerUpType.SLOW_MOTION:
            self.speed = max(3, self.base_speed // 2)
        elif effect_type == PowerUpType.INVINCIBLE:
            self.invincible = True
        elif effect_type == PowerUpType.SHRINK:
            if len(self.snake_body) > 3:
                self.snake_body = self.snake_body[:len(self.snake_body)//2]
        elif effect_type == PowerUpType.TELEPORT:
            # 随机传送蛇头
            new_pos = self.generate_food()
            self.snake_body[0] = new_pos
        elif effect_type == PowerUpType.FREEZE:
            self.frozen = True

        self.sound_manager.play('powerup')

        # 检查道具大师成就
        if len(self.achievements.used_powerups) >= len(PowerUpType):
            self.achievements.check_achievement('powerup_master')

    def update_effects(self):
        """更新道具效果"""
        current_time = time.time()
        expired_effects = []

        for effect_type, end_time in self.active_effects.items():
            if current_time > end_time:
                expired_effects.append(effect_type)

        for effect_type in expired_effects:
            del self.active_effects[effect_type]

            # 移除效果
            if effect_type in [PowerUpType.SPEED_BOOST, PowerUpType.SLOW_MOTION]:
                self.speed = self.base_speed
            elif effect_type == PowerUpType.INVINCIBLE:
                self.invincible = False
            elif effect_type == PowerUpType.FREEZE:
                self.frozen = False

    def handle_input(self, event):
        """处理输入"""
        if event.type == pygame.KEYDOWN:
            if self.game_state == 'menu':
                if event.key == pygame.K_UP:
                    self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    self.game_mode = self.menu_options[self.menu_selected]
                    self.game_state = 'playing'
                    self.reset_game()
                    self.stats['games_played'] += 1
                elif event.key == pygame.K_s:
                    # 切换皮肤
                    skins = list(self.snake_skin.skins.keys())
                    current_index = skins.index(self.snake_skin.current_skin)
                    self.snake_skin.current_skin = skins[(current_index + 1) % len(skins)]
                    self.achievements.used_skins.add(self.snake_skin.current_skin)

                    if len(self.achievements.used_skins) >= len(skins):
                        self.achievements.check_achievement('shapeshifter')

            elif self.game_state == 'playing':
                # 方向控制
                if event.key == pygame.K_UP and self.snake_direction != Direction.DOWN:
                    self.snake_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.snake_direction != Direction.UP:
                    self.snake_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.snake_direction != Direction.RIGHT:
                    self.snake_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.snake_direction != Direction.LEFT:
                    self.snake_direction = Direction.RIGHT
                elif event.key == pygame.K_p:
                    self.game_state = 'paused'
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = 'menu'

            elif self.game_state == 'paused':
                if event.key == pygame.K_p:
                    self.game_state = 'playing'
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = 'menu'

            elif self.game_state == 'game_over':
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.game_state = 'playing'
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = 'menu'

    def update_game(self, dt: float):
        """更新游戏逻辑"""
        if self.game_state != 'playing':
            return

        self.game_time += dt

        # 更新道具效果
        self.update_effects()

        # 检查生存成就
        if self.game_time > 300:  # 5分钟
            self.achievements.check_achievement('survivor')

        # 生成道具
        if (time.time() - self.last_powerup_spawn > 10 and
            random.random() < 0.3):  # 30%概率每10秒
            self.spawn_powerup()
            self.last_powerup_spawn = time.time()

        # 更新道具
        for powerup in self.powerups[:]:
            powerup.lifetime -= dt
            if powerup.lifetime <= 0:
                self.powerups.remove(powerup)

        # 移动蛇（如果没有被冰冻）
        if not self.frozen and time.time() - self.last_move_time > 1.0 / self.speed:
            self.move_snake()
            self.last_move_time = time.time()

        # 更新AI蛇（对战模式）
        if self.game_mode == GameMode.BATTLE:
            self.update_ai_snake()

        # 更新粒子系统
        self.particle_system.update(dt)

        # 更新屏幕震动
        if self.screen_shake > 0:
            self.screen_shake -= dt * 10

    def move_snake(self):
        """移动蛇"""
        # 计算新头部位置
        head_x, head_y = self.snake_body[0]
        dx, dy = self.snake_direction.value
        new_head = (head_x + dx, head_y + dy)

        # 边界处理
        if self.game_mode == GameMode.CLASSIC:
            # 经典模式：穿墙
            new_head = (new_head[0] % self.GRID_WIDTH, new_head[1] % self.GRID_HEIGHT)
        else:
            # 其他模式：撞墙死亡
            if (new_head[0] < 0 or new_head[0] >= self.GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= self.GRID_HEIGHT):
                if not self.invincible:
                    self.game_over()
                    return
                else:
                    # 无敌状态下反弹
                    new_head = (head_x, head_y)
                    self.snake_direction = Direction((-dx, -dy))

        # 检查撞到自己
        if new_head in self.snake_body[1:] and not self.invincible:
            self.game_over()
            return

        # 检查撞到墙壁
        if new_head in self.walls and not self.invincible:
            self.game_over()
            return

        # 添加新头部
        self.snake_body.insert(0, new_head)

        # 添加尾迹效果
        head_pixel_x = new_head[0] * self.GRID_SIZE + self.GRID_SIZE // 2
        head_pixel_y = new_head[1] * self.GRID_SIZE + self.GRID_SIZE // 2
        self.particle_system.add_trail(head_pixel_x, head_pixel_y,
                                     self.snake_skin.skins[self.snake_skin.current_skin]['head'])

        # 检查吃到食物
        if new_head == self.food_pos:
            self.eat_food()
        else:
            # 检查吃到道具
            for powerup in self.powerups[:]:
                if new_head == powerup.pos:
                    self.apply_powerup(powerup)
                    self.powerups.remove(powerup)

                    # 粒子效果
                    pixel_x = powerup.pos[0] * self.GRID_SIZE + self.GRID_SIZE // 2
                    pixel_y = powerup.pos[1] * self.GRID_SIZE + self.GRID_SIZE // 2
                    self.particle_system.add_explosion(pixel_x, pixel_y, powerup.color, 20)
                    break

            # 移除尾部（如果没有待生长的段）
            if self.grow_pending > 0:
                self.grow_pending -= 1
            else:
                self.snake_body.pop()

    def eat_food(self):
        """吃到食物"""
        self.score += 10 * self.level

        # 双倍分数效果
        if PowerUpType.DOUBLE_SCORE in self.active_effects:
            self.score += 10 * self.level

        self.food_eaten += 1
        self.stats['total_food_eaten'] += 1
        self.grow_pending += 1

        # 生成新食物
        self.food_pos = self.generate_food()

        # 增加速度和等级
        if self.food_eaten % 5 == 0:
            self.level += 1
            self.base_speed = min(25, self.base_speed + 1)
            if PowerUpType.SPEED_BOOST not in self.active_effects and PowerUpType.SLOW_MOTION not in self.active_effects:
                self.speed = self.base_speed

        # 音效和粒子效果
        self.sound_manager.play('eat')
        food_pixel_x = self.food_pos[0] * self.GRID_SIZE + self.GRID_SIZE // 2
        food_pixel_y = self.food_pos[1] * self.GRID_SIZE + self.GRID_SIZE // 2
        self.particle_system.add_explosion(food_pixel_x, food_pixel_y, (255, 255, 0), 15)

        # 检查成就
        self.achievements.check_achievement('first_food', self.food_eaten >= 1)
        self.achievements.check_achievement('century', self.food_eaten >= 100)

        if self.speed >= 25:
            self.achievements.check_achievement('speed_demon')

    def update_ai_snake(self):
        """更新AI蛇"""
        # 简单AI：朝食物移动
        obstacles = self.snake_body + self.walls
        new_direction = self.ai_snake.find_path_to_food(self.food_pos, obstacles)

        if new_direction:
            self.ai_snake.direction = new_direction

            # 移动AI蛇
            head_x, head_y = self.ai_snake.body[0]
            dx, dy = self.ai_snake.direction.value
            new_head = (head_x + dx, head_y + dy)

            # 边界检查
            if (0 <= new_head[0] < self.GRID_WIDTH and
                0 <= new_head[1] < self.GRID_HEIGHT and
                new_head not in self.ai_snake.body and
                new_head not in self.walls):

                self.ai_snake.body.insert(0, new_head)

                # 检查AI吃到食物
                if new_head == self.food_pos:
                    self.food_pos = self.generate_food()
                else:
                    self.ai_snake.body.pop()

    def game_over(self):
        """游戏结束"""
        self.game_state = 'game_over'
        self.sound_manager.play('death')

        # 屏幕震动
        self.screen_shake = 1.0

        # 爆炸效果
        for segment in self.snake_body:
            pixel_x = segment[0] * self.GRID_SIZE + self.GRID_SIZE // 2
            pixel_y = segment[1] * self.GRID_SIZE + self.GRID_SIZE // 2
            self.particle_system.add_explosion(pixel_x, pixel_y, (255, 0, 0), 10)

        # 更新统计
        if self.score > self.stats['highest_score']:
            self.stats['highest_score'] = self.score

        self.save_stats()

    def save_stats(self):
        """保存统计数据"""
        try:
            with open('snake_stats.json', 'w') as f:
                json.dump(self.stats, f)
        except:
            pass  # 忽略保存错误

    def load_stats(self):
        """加载统计数据"""
        try:
            if os.path.exists('snake_stats.json'):
                with open('snake_stats.json', 'r') as f:
                    self.stats.update(json.load(f))
        except:
            pass  # 忽略加载错误

    def render_game(self):
        """渲染游戏"""
        # 屏幕震动效果
        shake_x = shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-int(self.screen_shake * 10), int(self.screen_shake * 10))
            shake_y = random.randint(-int(self.screen_shake * 10), int(self.screen_shake * 10))

        # 背景
        self.screen.fill((20, 20, 40))

        # 网格线（可选）
        if self.game_mode == GameMode.ZEN:
            for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
                pygame.draw.line(self.screen, (40, 40, 60),
                               (x + shake_x, shake_y), (x + shake_x, self.WINDOW_HEIGHT + shake_y))
            for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
                pygame.draw.line(self.screen, (40, 40, 60),
                               (shake_x, y + shake_y), (self.WINDOW_WIDTH + shake_x, y + shake_y))

        # 渲染墙壁
        for wall in self.walls:
            wall_rect = pygame.Rect(wall[0] * self.GRID_SIZE + shake_x,
                                  wall[1] * self.GRID_SIZE + shake_y,
                                  self.GRID_SIZE, self.GRID_SIZE)
            pygame.draw.rect(self.screen, (100, 100, 100), wall_rect)
            pygame.draw.rect(self.screen, (150, 150, 150), wall_rect, 2)

        # 渲染食物
        food_rect = pygame.Rect(self.food_pos[0] * self.GRID_SIZE + shake_x,
                              self.food_pos[1] * self.GRID_SIZE + shake_y,
                              self.GRID_SIZE, self.GRID_SIZE)

        # 食物发光效果
        glow_rect = food_rect.inflate(6, 6)
        temp_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(temp_surface, (255, 100, 100, 100),
                          (0, 0, glow_rect.width, glow_rect.height))
        self.screen.blit(temp_surface, glow_rect.topleft)

        pygame.draw.ellipse(self.screen, (255, 50, 50), food_rect)
        pygame.draw.ellipse(self.screen, (255, 150, 150), food_rect, 3)

        # 渲染道具
        for powerup in self.powerups:
            powerup_rect = pygame.Rect(powerup.pos[0] * self.GRID_SIZE + shake_x,
                                     powerup.pos[1] * self.GRID_SIZE + shake_y,
                                     self.GRID_SIZE, self.GRID_SIZE)

            # 道具闪烁效果
            alpha = int(127 + 127 * math.sin(time.time() * 5))
            temp_surface = pygame.Surface((self.GRID_SIZE, self.GRID_SIZE), pygame.SRCALPHA)
            pygame.draw.ellipse(temp_surface, (*powerup.color, alpha),
                              (0, 0, self.GRID_SIZE, self.GRID_SIZE))
            self.screen.blit(temp_surface, powerup_rect.topleft)

            # 道具图标（简单文字）
            icon_text = {
                PowerUpType.SPEED_BOOST: "S",
                PowerUpType.SLOW_MOTION: "T",
                PowerUpType.INVINCIBLE: "I",
                PowerUpType.DOUBLE_SCORE: "2",
                PowerUpType.SHRINK: "↓",
                PowerUpType.TELEPORT: "T",
                PowerUpType.FREEZE: "F"
            }

            icon = self.font_small.render(icon_text[powerup.type], True, (255, 255, 255))
            icon_rect = icon.get_rect(center=powerup_rect.center)
            self.screen.blit(icon, icon_rect)

        # 渲染蛇
        current_time = time.time()
        for i, segment in enumerate(self.snake_body):
            segment_rect = pygame.Rect(segment[0] * self.GRID_SIZE + shake_x,
                                     segment[1] * self.GRID_SIZE + shake_y,
                                     self.GRID_SIZE, self.GRID_SIZE)

            is_head = (i == 0)
            self.snake_skin.render_segment(self.screen, segment_rect, is_head,
                                         i, len(self.snake_body), current_time)

            # 无敌效果
            if self.invincible and is_head:
                glow_rect = segment_rect.inflate(4, 4)
                temp_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                alpha = int(100 + 100 * math.sin(time.time() * 10))
                pygame.draw.rect(temp_surface, (255, 255, 0, alpha),
                               (0, 0, glow_rect.width, glow_rect.height), border_radius=8)
                self.screen.blit(temp_surface, glow_rect.topleft)

        # 渲染AI蛇（对战模式）
        if self.game_mode == GameMode.BATTLE:
            for i, segment in enumerate(self.ai_snake.body):
                segment_rect = pygame.Rect(segment[0] * self.GRID_SIZE + shake_x,
                                         segment[1] * self.GRID_SIZE + shake_y,
                                         self.GRID_SIZE, self.GRID_SIZE)

                color = (255, 100, 100) if i == 0 else (200, 80, 80)
                pygame.draw.rect(self.screen, color, segment_rect, border_radius=5)

        # 渲染粒子效果
        self.particle_system.render(self.screen)

        # 渲染UI
        self.render_ui()

        # 渲染成就通知
        current_time = time.time()
        self.achievements.update_notifications(current_time)
        self.achievements.render_notifications(self.screen, self.font_small)

    def render_ui(self):
        """渲染用户界面"""
        # 分数
        score_text = self.font_medium.render(f"分数: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # 等级
        level_text = self.font_small.render(f"等级: {self.level}", True, (200, 200, 255))
        self.screen.blit(level_text, (10, 50))

        # 食物计数
        food_text = self.font_small.render(f"食物: {self.food_eaten}", True, (255, 200, 200))
        self.screen.blit(food_text, (10, 75))

        # 速度
        speed_text = self.font_small.render(f"速度: {self.speed}", True, (200, 255, 200))
        self.screen.blit(speed_text, (10, 100))

        # 游戏模式
        mode_text = self.font_small.render(f"模式: {self.game_mode.value}", True, (255, 255, 200))
        self.screen.blit(mode_text, (10, 125))

        # 皮肤
        skin_text = self.font_small.render(f"皮肤: {self.snake_skin.current_skin.title()}", True, (255, 200, 255))
        self.screen.blit(skin_text, (10, 150))

        # 活跃效果
        y_offset = 180
        for effect_type, end_time in self.active_effects.items():
            remaining = max(0, end_time - time.time())
            effect_text = self.font_small.render(f"{effect_type.value}: {remaining:.1f}s", True, (255, 255, 0))
            self.screen.blit(effect_text, (10, y_offset))
            y_offset += 20

        # 最高分（右上角）
        high_score_text = self.font_small.render(f"最高分: {self.stats['highest_score']}", True, (255, 215, 0))
        self.screen.blit(high_score_text, (self.WINDOW_WIDTH - 150, 10))

        # 游戏时间
        time_text = self.font_small.render(f"时间: {int(self.game_time)}s", True, (200, 200, 200))
        self.screen.blit(time_text, (self.WINDOW_WIDTH - 150, 35))

    def render_menu(self):
        """渲染主菜单"""
        self.screen.fill((10, 10, 30))

        # 标题
        title = self.font_large.render("Hello,welcom to the King of Snake", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        subtitle = self.font_medium.render("Ultimate Snake Game", True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(self.WINDOW_WIDTH // 2, 140))
        self.screen.blit(subtitle, subtitle_rect)

        # 游戏模式选项
        y_start = 200
        for i, mode in enumerate(self.menu_options):
            color = (255, 255, 0) if i == self.menu_selected else (255, 255, 255)
            text = self.font_medium.render(mode.value, True, color)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_start + i * 50))
            self.screen.blit(text, text_rect)

            # 选中指示器
            if i == self.menu_selected:
                pygame.draw.circle(self.screen, (255, 255, 0),
                                 (text_rect.left - 30, text_rect.centery), 5)

        # 控制说明
        controls = [
            "↑↓ 选择模式    Enter 开始游戏",
            "S 切换皮肤     Esc 退出",
            "P 暂停游戏     R 重新开始"
        ]

        y_start = self.WINDOW_HEIGHT - 150
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (150, 150, 150))
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_start + i * 25))
            self.screen.blit(text, text_rect)

        # 统计信息
        stats_y = self.WINDOW_HEIGHT - 250
        stats_text = [
            f"游戏次数: {self.stats['games_played']}",
            f"总食物: {self.stats['total_food_eaten']}",
            f"最高分: {self.stats['highest_score']}"
        ]

        for i, stat in enumerate(stats_text):
            text = self.font_small.render(stat, True, (100, 200, 100))
            self.screen.blit(text, (50, stats_y + i * 20))

        # 当前皮肤预览
        skin_preview_x = self.WINDOW_WIDTH - 200
        skin_preview_y = 200

        preview_text = self.font_small.render("当前皮肤:", True, (255, 255, 255))
        self.screen.blit(preview_text, (skin_preview_x, skin_preview_y))

        # 绘制皮肤预览
        for i in range(5):
            rect = pygame.Rect(skin_preview_x + i * 25, skin_preview_y + 30, 20, 20)
            is_head = (i == 0)
            self.snake_skin.render_segment(self.screen, rect, is_head, i, 5, time.time())

    def render_pause(self):
        """渲染暂停画面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 暂停文字
        pause_text = self.font_large.render("游戏暂停", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

        # 提示文字
        hint_text = self.font_small.render("按 P 继续游戏，Esc 返回主菜单", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(hint_text, hint_rect)

    def render_game_over(self):
        """渲染游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((50, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字
        game_over_text = self.font_large.render("游戏结束", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)

        # 最终分数
        score_text = self.font_medium.render(f"最终分数: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)

        # 统计信息
        stats = [
            f"等级: {self.level}",
            f"食物: {self.food_eaten}",
            f"时间: {int(self.game_time)}秒",
            f"蛇长: {len(self.snake_body)}"
        ]

        for i, stat in enumerate(stats):
            text = self.font_small.render(stat, True, (200, 200, 200))
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + i * 25))
            self.screen.blit(text, text_rect)

        # 提示文字
        hint_text = self.font_small.render("按 R 重新开始，Esc 返回主菜单", True, (255, 255, 0))
        hint_rect = hint_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 150))
        self.screen.blit(hint_text, hint_rect)

    def run(self):
        """主游戏循环"""
        clock = pygame.time.Clock()
        running = True

        print("🐍 欢迎来到无敌蛇王 - Ultimate Snake Game!")
        print("🌟 特色功能:")
        print("   • 6种游戏模式：经典、极速、迷宫、对战、生存、禅意")
        print("   • 6种华丽皮肤：经典、彩虹、霓虹、火焰、冰霜、星空")
        print("   • 7种神奇道具：加速、缓慢、无敌、双倍分数、缩小、传送、冰冻")
        print("   • 粒子效果系统、动态音效、成就系统")
        print("   • AI对战模式、统计数据保存")
        print("🎮 控制说明:")
        print("   • 方向键：移动蛇")
        print("   • P键：暂停/继续")
        print("   • S键：切换皮肤（主菜单）")
        print("   • R键：重新开始（游戏结束）")
        print("   • Esc键：返回主菜单")
        print("🎯 准备好挑战史上最华丽的贪吃蛇了吗？")

        while running:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_input(event)

            # 更新游戏
            if self.game_state == 'playing':
                self.update_game(dt)

            # 渲染
            if self.game_state == 'menu':
                self.render_menu()
            elif self.game_state == 'playing':
                self.render_game()

                # 覆盖渲染暂停和游戏结束
                if self.game_state == 'paused':
                    self.render_pause()
                elif self.game_state == 'game_over':
                    self.render_game_over()
            elif self.game_state == 'paused':
                self.render_game()
                self.render_pause()
            elif self.game_state == 'game_over':
                self.render_game()
                self.render_game_over()

            pygame.display.flip()

        # 保存统计数据
        self.save_stats()
        pygame.quit()
        print("👋 感谢体验无敌蛇王！")
