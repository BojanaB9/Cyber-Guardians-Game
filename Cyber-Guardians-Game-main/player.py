import pygame
import os
from entities import load_strip, AnimatedSprite

class Player(AnimatedSprite):
    def __init__(self, settings):
        self.settings = settings

        # 7 frames of 32x40
        frames = load_strip(
            os.path.join("assets", "player_spaceship_1.png"),
            frame_w=32,
            frame_h=40,
            scale_to=(70, 90)
        )

        super().__init__(frames, fps=12)
        self.rect = self.image.get_rect(center=(100, 300))

    def update(self, keys):
        self.animate()

        speed = self.settings.player_speed

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 900:
            self.rect.x += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < 600:
            self.rect.y += speed