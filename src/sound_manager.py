from pathlib import Path
import pygame
import os

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets" / "sounds"

class SoundManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(current_dir), "assets", "sounds")

        self.sounds = {}
        sound_files = {
            "bgm": "bgm.wav",
            "start": "click.wav",
            "high_score": "high_score.wav",
            "botHigh_score": "botHigh_score.wav",
            "upLow_score": "upLow_score.wav",
            "low_score": "low_score.wav",
        }

        for sound_name, filename in sound_files.items():
            filepath = os.path.join(assets_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                except Exception as e:
                    print(f"Could not load sound '{filename}': {e}")
            else:
                print(f"Sound file not found: {filepath}")

    def play(self, sound_name, loops=0):
        """Mainkan suara berdasarkan nama yang terdaftar.
        Args:
            sound_name: Nama suara yang akan dimainkan
            loops: Jumlah pengulangan (-1 untuk loop tanpa batas, 0 untuk sekali)
        """
        sound = self.sounds.get(sound_name)
        if sound:
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
