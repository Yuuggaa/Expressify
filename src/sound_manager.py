from pathlib import Path
import pygame
import os
import sys
import numpy as np

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

# Get base path for assets (works with PyInstaller)
def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return Path(__file__).resolve().parent.parent

PROJECT_ROOT = get_base_path()
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "sounds")

class SoundManager:
    def __init__(self):
        assets_dir = ASSETS_DIR

        self.sounds = {}
        self.trimmed_sounds = {}  # Untuk menyimpan versi trimmed
        sound_files = {
            "bgm": "bgm.wav",
            "start": "click.wav",
            "high_score": "high_score.wav",
            "botHigh_score": "botHigh_score.wav",
            "upLow_score": "upLow_score.wav",
            "low_score": "low_score.wav",
            "true_answer": "true.wav",
        }

        for sound_name, filename in sound_files.items():
            filepath = os.path.join(assets_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    
                    # Buat versi trimmed untuk suara click (mulai dari pertengahan)
                    if sound_name == "start":
                        self.trimmed_sounds[sound_name] = self.trim_sound(filepath, start_percent=0.62)
                    if sound_name == "true_answer":
                        self.trimmed_sounds[sound_name] = self.trim_sound(filepath, start_percent=0.5)
                    
                    # Set volume untuk suara tertentu
                    if sound_name == "true_answer":
                        self.sounds[sound_name].set_volume(0.8)  # Volume 80%
                    elif sound_name == "bgm":
                        self.sounds[sound_name].set_volume(0.3)  # BGM lebih pelan
                    elif sound_name == "start":
                        self.sounds[sound_name].set_volume(1.0)  # Click full volume
                        if sound_name in self.trimmed_sounds:
                            self.trimmed_sounds[sound_name].set_volume(1.0)
                except Exception as e:
                    print(f"Could not load sound '{filename}': {e}")
            else:
                print(f"Sound file not found: {filepath}")
    
    def trim_sound(self, filepath, start_percent=0.3):
        try:
            # Load sound sebagai array
            sound = pygame.mixer.Sound(filepath)
            sound_array = pygame.sndarray.array(sound)
            
            # Hitung posisi mulai
            start_frame = int(len(sound_array) * start_percent)
            
            # Potong array dari posisi start
            trimmed_array = sound_array[start_frame:]
            
            # Buat Sound baru dari array yang sudah dipotong
            trimmed_sound = pygame.sndarray.make_sound(trimmed_array)
            return trimmed_sound
        except Exception as e:
            print(f"Could not trim sound: {e}")
            return sound  # Return original jika gagal

    def play(self, sound_name, loops=0, volume=None, start_pos=0.0):
        """Mainkan suara berdasarkan nama yang terdaftar.
        Args:
            sound_name: Nama suara yang akan dimainkan
            loops: Jumlah pengulangan (-1 untuk loop tanpa batas, 0 untuk sekali)
            volume: Volume override (0.0 - 1.0), jika None gunakan volume default
            start_pos: Tidak digunakan lagi (diganti dengan trimmed_sounds)
        """
        # Untuk suara click/start, gunakan versi trimmed jika ada
        if sound_name in self.trimmed_sounds:
            sound = self.trimmed_sounds[sound_name]
        else:
            sound = self.sounds.get(sound_name)
            
        if sound:
            if volume is not None:
                sound.set_volume(volume)
            sound.play(loops=loops)
        else:
            print(f"Sound '{sound_name}' tidak tersedia.")

    def stop(self, sound_name):
        """Hentikan suara tertentu jika sedang dimainkan."""
        sound = self.sounds.get(sound_name)
        if sound:
            sound.stop()
        else:
            print(f"[WARNING] Sound '{sound_name}' tidak ditemukan atau belum dimuat.")
