"""
AI蛇系统
"""

import random
from typing import List, Tuple
from .enums import Direction

class AISnake:
    """AI蛇（简单的路径查找）"""
    
    def __init__(self, start_pos: Tuple[int, int], grid_size: int):
        self.body = [start_pos]
        self.direction = Direction.RIGHT
        self.grid_size = grid_size
        self.target = None
    
    def find_path_to_food(self, food_pos: Tuple[int, int], obstacles: List[Tuple[int, int]]) -> Direction:
        """简单的A*路径查找"""
        head_x, head_y = self.body[0]
        food_x, food_y = food_pos
        
        # 简化版：朝着食物方向移动，避开障碍物
        dx = food_x - head_x
        dy = food_y - head_y
        
        # 优先级：距离更近的方向
        possible_moves = []
        
        if dx > 0:
            possible_moves.append((Direction.RIGHT, abs(dx)))
        elif dx < 0:
            possible_moves.append((Direction.LEFT, abs(dx)))
        
        if dy > 0:
            possible_moves.append((Direction.DOWN, abs(dy)))
        elif dy < 0:
            possible_moves.append((Direction.UP, abs(dy)))
        
        # 按距离排序
        possible_moves.sort(key=lambda x: x[1], reverse=True)
        
        # 检查每个方向是否安全
        for direction, _ in possible_moves:
            new_x = head_x + direction.value[0]
            new_y = head_y + direction.value[1]
            
            # 检查边界
            if (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size):
                # 检查是否撞到自己或障碍物
                if (new_x, new_y) not in self.body and (new_x, new_y) not in obstacles:
                    return direction
        
        # 如果没有安全路径，随机选择
        safe_directions = []
        for direction in Direction:
            new_x = head_x + direction.value[0]
            new_y = head_y + direction.value[1]
            
            if (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size):
                if (new_x, new_y) not in self.body and (new_x, new_y) not in obstacles:
                    safe_directions.append(direction)
        
        return random.choice(safe_directions) if safe_directions else Direction.RIGHT
