"""
贪吃蛇游戏枚举类型定义
"""

from enum import Enum
from typing import Tuple
from dataclasses import dataclass

class Direction(Enum):
    """方向枚举"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameMode(Enum):
    """游戏模式"""
    CLASSIC = "经典模式"
    SPEED = "极速模式"
    MAZE = "迷宫模式"
    BATTLE = "对战模式"
    SURVIVAL = "生存模式"
    ZEN = "禅意模式"

class PowerUpType(Enum):
    """道具类型"""
    SPEED_BOOST = "加速"
    SLOW_MOTION = "缓慢"
    INVINCIBLE = "无敌"
    DOUBLE_SCORE = "双倍分数"
    SHRINK = "缩小"
    TELEPORT = "传送"
    FREEZE = "冰冻"

@dataclass
class PowerUp:
    """道具类"""
    pos: Tuple[int, int]
    type: PowerUpType
    color: Tuple[int, int, int]
    lifetime: float
    effect_duration: float = 5.0
