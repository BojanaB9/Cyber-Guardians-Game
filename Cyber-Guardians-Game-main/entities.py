import pygame
import random
import os
import math


# Помошна функција за вчитување на Sprite листови (Animation Strips)
def load_strip(path, frame_w, frame_h, scale_to=None):
    try:
        sheet = pygame.image.load(path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()
        frames = []
        for x in range(0, sheet_w, frame_w):
            frame = sheet.subsurface(pygame.Rect(x, 0, frame_w, frame_h)).copy()
            if scale_to:
                frame = pygame.transform.smoothscale(frame, scale_to)
            frames.append(frame)
        return frames
    except Exception as e:
        print(f"Грешка при вчитување на {path}: {e}")
        # Враќаме празна површина ако фајлот не постои за да не крашне играта
        surf = pygame.Surface(scale_to if scale_to else (32, 32))
        surf.fill((255, 0, 255))
        return [surf]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = settings.bullet_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Класа која служи како основа за сите анимирани објекти
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, fps=12):
        super().__init__()
        self.frames = frames
        self.fps = fps
        self.frame_i = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self._frame_ms = int(1000 / fps)
        self._last = pygame.time.get_ticks()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self._last >= self._frame_ms:
            self._last = now
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            old_center = self.rect.center
            self.image = self.frames[self.frame_i]
            self.rect = self.image.get_rect(center=old_center)


class Enemy(AnimatedSprite):  # СМЕНЕТО: Сега наследува од AnimatedSprite
    def __init__(self, settings, is_special=False):
        self.is_special = is_special
        self.hp = 3 if is_special else 1

        # Вчитување соодветни фрејмови
        if not is_special:
            frames = load_strip(
                os.path.join("assets", "enemy_spaceship_2.png"),
                frame_w=32, frame_h=32, scale_to=(48, 48)
            )
        else:
            frames = load_strip(
                os.path.join("assets", "enemy_spaceship_5.png"),
                frame_w=32, frame_h=40, scale_to=(48, 60)
            )

        # Иницијализација на AnimatedSprite
        super().__init__(frames, fps=10)

        # Позиционирање
        self.rect.x = random.randint(0, 900 - self.rect.width)
        self.rect.y = -self.rect.height

        # Брзина (се зголемува со нивото)
        base_speed = random.uniform(2.0, 4.0)
        self.speed = base_speed + (settings.current_level * 0.2)

    def update(self):
        self.animate()
        self.rect.y += self.speed
        if self.rect.top > 700:
            self.kill()


class KnowledgeDrop(pygame.sprite.Sprite):
    _image = None

    def __init__(self, x, y, available_info):
        super().__init__()

        # Решаваме проблем ако листата е празна
        if available_info and len(available_info) > 0:
            self.text = available_info.pop(0)
        else:
            self.text = "Знењето е моќ! Подготви се за квизот!"

        if KnowledgeDrop._image is None:
            try:
                img = pygame.image.load(os.path.join("assets", "gem.png")).convert_alpha()
                KnowledgeDrop._image = pygame.transform.smoothscale(img, (28, 28))
            except:
                KnowledgeDrop._image = pygame.Surface((28, 28))
                KnowledgeDrop._image.fill((0, 255, 0))

        self.image = KnowledgeDrop._image
        self.rect = self.image.get_rect(center=(x, y))
        self.t = 0  # За синусоидно движење (лебдење)

    def update(self):
        # Паѓање со лесно лебдење лево-десно
        self.t += 0.1
        self.rect.y += 2
        self.rect.x += math.sin(self.t) * 1.5

        if self.rect.top > 700:
            self.kill()