import pygame

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

class SoundManager:
    def __init__(self):
        self.sounds = {
            "bgm": pygame.mixer.Sound("../assets/sounds/bgm.wav"),
            "high_score": pygame.mixer.Sound("../assets/sounds/high_score.wav"),
            "botHigh_score": pygame.mixer.Sound("../assets/sounds/botHigh_score.wav"),
            "upLow_score": pygame.mixer.Sound("../assets/sounds/upLow_score.wav"),
            "low_score": pygame.mixer.Sound("../assets/sounds/low_score.wav"),
        }

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' tidak ditemukan.")

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
