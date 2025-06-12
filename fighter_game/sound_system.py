"""
音效系统
"""

import pygame
import numpy as np

# 音效配置
LOADED_SOUNDS = {}

def generate_sound(frequency, duration_ms, shape='square', volume=0.3):
    """生成一个简单的音效并返回 pygame.mixer.Sound 对象"""
    sample_rate, format_bits, channels = pygame.mixer.get_init()
    if sample_rate == 0:  # Mixer not initialized or failed
        print("警告: Pygame Mixer 未正确初始化，无法生成声音。")
        return None

    num_samples = int(sample_rate * duration_ms / 1000.0)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Max amplitude for int16 is 32767. Apply volume.
    amplitude = int(32767 * volume) 

    if shape == 'square':
        period_samples = sample_rate / frequency
        for i in range(num_samples):
            if (i // (period_samples / 2)) % 2 == 0:
                arr[i] = amplitude
            else:
                arr[i] = -amplitude
    elif shape == 'sine':  # Example for a sine wave
        for i in range(num_samples):
            arr[i] = int(amplitude * np.sin(2 * np.pi * frequency * i / sample_rate))
    # Can add other shapes like 'sawtooth', 'triangle' if needed

    if channels == 2:  # Stereo
        stereo_arr = np.zeros((num_samples, 2), dtype=np.int16)
        stereo_arr[:,0] = arr
        stereo_arr[:,1] = arr
        sound_buffer = stereo_arr
    else:  # Mono
        sound_buffer = arr
    
    try:
        sound = pygame.mixer.Sound(buffer=sound_buffer)
        return sound
    except pygame.error as e:
        print(f"警告: 创建Sound对象失败: {e}")
        return None

def initialize_sounds():
    """初始化音效系统"""
    pygame.mixer.init()
    
    # 尝试在mixer初始化后立即生成声音
    if pygame.mixer.get_init():  # Check if mixer was successfully initialized
        LOADED_SOUNDS["punch"] = generate_sound(660, 80, shape='square', volume=0.25)
        LOADED_SOUNDS["kick"]  = generate_sound(550, 100, shape='square', volume=0.3)
        LOADED_SOUNDS["hit"]   = generate_sound(330, 120, shape='square', volume=0.35)
        LOADED_SOUNDS["jump"]  = generate_sound(880, 70, shape='square', volume=0.2)
        LOADED_SOUNDS["special"] = generate_sound(440, 150, shape='sine', volume=0.4)
        LOADED_SOUNDS["block"] = generate_sound(200, 60, shape='square', volume=0.2)
        LOADED_SOUNDS["ultimate"] = generate_sound(800, 200, shape='sine', volume=0.5)
        
        # 打印加载成功的音效（如果生成成功）
        for name, sound_obj in LOADED_SOUNDS.items():
            if sound_obj:
                print(f"成功生成内置音效: {name}")
            else:
                print(f"警告: 未能生成内置音效: {name}")
    else:
        print("警告: Pygame Mixer 初始化失败，将无声音运行。")

def play_sound(name):
    """播放音效 (如果已加载/生成)"""
    if name in LOADED_SOUNDS and LOADED_SOUNDS[name]:
        LOADED_SOUNDS[name].play()

def toggle_fullscreen():
    """切换全屏/窗口模式"""
    from .constants import SCREEN_WIDTH, SCREEN_HEIGHT
    global screen, is_fullscreen
    
    # 这个函数需要在主游戏类中实现
    pass
