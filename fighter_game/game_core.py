"""
格斗游戏核心逻辑
"""

import pygame
import sys
from .constants import *
from .game_data import game_data
from .sound_system import initialize_sounds, play_sound

class FighterGame:
    """格斗游戏主类"""
    
    def __init__(self):
        pygame.init()
        
        # 初始化显示
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("火柴人对打小游戏")
        self.clock = pygame.time.Clock()
        
        # 初始化音效系统
        initialize_sounds()
        
        # 字体设置
        try:
            font_path_simhei = pygame.font.match_font("simhei")
            if font_path_simhei:
                self.font = pygame.font.Font(font_path_simhei, 30)
                print(f"成功加载 SimHei 字体: {font_path_simhei}")
            else:
                raise pygame.error("SimHei not found by match_font")
        except pygame.error:
            try:
                font_path_msyh = pygame.font.match_font("microsoftyahei")
                if font_path_msyh:
                    self.font = pygame.font.Font(font_path_msyh, 30)
                    print(f"成功加载 Microsoft YaHei 字体: {font_path_msyh}")
                else:
                    raise pygame.error("Microsoft YaHei not found")
            except pygame.error:
                self.font = pygame.font.Font(None, 30)
                print("警告: 未找到中文字体，使用默认字体。")
        
        # 游戏状态
        self.game_state = "menu"  # menu, character_select, playing, shop, boss_mode
        self.selected_character = "warrior"
        self.menu_selection = 0
        self.menu_options = ["开始游戏", "角色选择", "装备商店", "Boss模式", "退出游戏"]
        
        # 全屏相关
        self.is_fullscreen = False
        self.original_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
        print("🥊 火柴人快打游戏初始化完成！")
    
    def toggle_fullscreen(self):
        """切换全屏/窗口模式"""
        global SCREEN_WIDTH, SCREEN_HEIGHT
        
        if self.is_fullscreen:
            # 切换到窗口模式
            self.screen = pygame.display.set_mode(self.original_size)
            self.is_fullscreen = False
            SCREEN_WIDTH, SCREEN_HEIGHT = self.original_size
            print("切换到窗口模式")
        else:
            # 切换到全屏模式
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True
            # 获取全屏尺寸
            info = pygame.display.Info()
            SCREEN_WIDTH = info.current_w
            SCREEN_HEIGHT = info.current_h
            print(f"切换到全屏模式 ({SCREEN_WIDTH}x{SCREEN_HEIGHT})")
        
        pygame.display.set_caption("火柴人对打小游戏")
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state == "menu":
                        return False
                    else:
                        self.game_state = "menu"
                
                # 菜单导航
                elif self.game_state == "menu":
                    if event.key == pygame.K_UP:
                        self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                        play_sound("jump")
                    elif event.key == pygame.K_DOWN:
                        self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                        play_sound("jump")
                    elif event.key == pygame.K_RETURN:
                        self.handle_menu_selection()
                        play_sound("punch")
        
        return True
    
    def handle_menu_selection(self):
        """处理菜单选择"""
        selected_option = self.menu_options[self.menu_selection]
        
        if selected_option == "开始游戏":
            self.game_state = "playing"
            print("开始游戏")
        elif selected_option == "角色选择":
            self.game_state = "character_select"
            print("角色选择")
        elif selected_option == "装备商店":
            self.game_state = "shop"
            print("装备商店")
        elif selected_option == "Boss模式":
            self.game_state = "boss_mode"
            print("Boss模式")
        elif selected_option == "退出游戏":
            pygame.quit()
            sys.exit()
    
    def update(self):
        """更新游戏逻辑"""
        if self.game_state == "playing":
            # 这里可以添加游戏逻辑
            pass
        elif self.game_state == "character_select":
            # 角色选择逻辑
            pass
        elif self.game_state == "shop":
            # 商店逻辑
            pass
        elif self.game_state == "boss_mode":
            # Boss模式逻辑
            pass
    
    def draw_menu(self):
        """绘制主菜单"""
        self.screen.fill(BLACK)
        
        # 标题
        title_text = self.font.render("火柴人快打", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # 菜单选项
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 60))
            self.screen.blit(option_text, option_rect)
        
        # 控制说明
        controls = [
            "↑↓ 选择菜单",
            "Enter 确认",
            "F11 全屏切换",
            "ESC 退出"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, LIGHT_GRAY)
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, 450 + i * 30))
            self.screen.blit(control_text, control_rect)
        
        # 游戏数据显示
        coin_text = self.font.render(f"金币: {game_data.coins}", True, GOLD)
        self.screen.blit(coin_text, (20, 20))
    
    def draw_character_select(self):
        """绘制角色选择界面"""
        self.screen.fill(DARK_BLUE)
        
        title_text = self.font.render("角色选择", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # 显示角色信息
        y_offset = 150
        for char_id, config in CHARACTER_CONFIGS.items():
            color = YELLOW if char_id == self.selected_character else WHITE
            char_text = self.font.render(f"{config['name']}: {config['description']}", True, color)
            char_rect = char_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(char_text, char_rect)
            y_offset += 40
    
    def draw_shop(self):
        """绘制商店界面"""
        self.screen.fill(DARK_GREEN)
        
        title_text = self.font.render("装备商店", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        coin_text = self.font.render(f"金币: {game_data.coins}", True, GOLD)
        self.screen.blit(coin_text, (20, 20))
    
    def draw_boss_mode(self):
        """绘制Boss模式界面"""
        self.screen.fill(DARK_RED)
        
        title_text = self.font.render("Boss模式", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
    
    def draw_playing(self):
        """绘制游戏界面"""
        self.screen.fill(BLUE)
        
        # 简单的游戏界面
        game_text = self.font.render("游戏进行中...", True, WHITE)
        game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_text, game_rect)
        
        hint_text = self.font.render("按 ESC 返回菜单", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(hint_text, hint_rect)
    
    def draw(self):
        """绘制游戏"""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "character_select":
            self.draw_character_select()
        elif self.game_state == "shop":
            self.draw_shop()
        elif self.game_state == "boss_mode":
            self.draw_boss_mode()
        elif self.game_state == "playing":
            self.draw_playing()
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        print("🥊 启动火柴人快打游戏...")
        print("🎮 控制说明:")
        print("   • ↑↓ 键：菜单导航")
        print("   • Enter：确认选择")
        print("   • F11：全屏切换")
        print("   • ESC：返回/退出")
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        print("👋 感谢体验火柴人快打！")
