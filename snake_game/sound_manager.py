"""
声音管理器
"""

import pygame
import numpy as np

class SoundManager:
    """声音管理器"""
    
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.create_sounds()
    
    def create_sounds(self):
        """创建程序化音效"""
        sr = 22050  # Sample rate
        
        # 吃食物音效 (简单上升音调)
        eat_freq_start = 440
        eat_freq_end = 880
        eat_duration = 0.1
        t = np.linspace(0, eat_duration, int(sr * eat_duration), False)
        eat_wave_mono = 0.5 * np.sin(2 * np.pi * np.linspace(eat_freq_start, eat_freq_end, len(t)) * t)
        eat_wave_mono *= np.exp(-5 * t)
        eat_wave_stereo = np.column_stack((eat_wave_mono, eat_wave_mono))
        eat_sound = pygame.sndarray.make_sound((eat_wave_stereo * 32767).astype(np.int16))
        self.sounds['eat'] = eat_sound
        
        # 游戏结束音效 (下降音调)
        death_freq_start = 880
        death_freq_end = 220
        death_duration = 0.5
        t = np.linspace(0, death_duration, int(sr * death_duration), False)
        death_wave_mono = 0.5 * np.sin(2 * np.pi * np.linspace(death_freq_start, death_freq_end, len(t)) * t)
        death_wave_mono *= np.exp(-3 * t)
        death_wave_stereo = np.column_stack((death_wave_mono, death_wave_mono))
        death_sound = pygame.sndarray.make_sound((death_wave_stereo * 32767).astype(np.int16))
        self.sounds['death'] = death_sound
        
        # 道具音效 (短促高音)
        powerup_freq = 1200
        powerup_duration = 0.05
        t = np.linspace(0, powerup_duration, int(sr * powerup_duration), False)
        powerup_wave_mono = 0.4 * np.sin(2 * np.pi * powerup_freq * t)
        powerup_wave_mono *= np.exp(-20 * t)
        powerup_wave_stereo = np.column_stack((powerup_wave_mono, powerup_wave_mono))
        powerup_sound = pygame.sndarray.make_sound((powerup_wave_stereo * 32767).astype(np.int16))
        self.sounds['powerup'] = powerup_sound
    
    def play(self, sound_name: str):
        """播放音效"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
