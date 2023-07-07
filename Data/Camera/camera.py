import pygame

class Camera:
    def __init__(self, player, screen_width, screen_height, level_width, level_height):
        self.player = player
        self.rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.level_width = level_width
        self.level_height = level_height

    def update(self):
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.level_width:
            self.rect.right = self.level_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.level_height:
            self.rect.bottom = self.level_height