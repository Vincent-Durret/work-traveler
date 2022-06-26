import pygame
from pygame import surface
from pygame.draw import rect





class Unit:
    def __init__(self, sprite, current_health=100, max_health=100):
        self.sprite = sprite
        self.rect = self.sprite.image.get_rect()
        self.current_health = current_health
        self.max_health = max_health





    def damage(self, amount):
        if self.current_health - amount > amount:
            self.current_health -= amount

    def is_dead(self):
        self.current_health = 0
        self.sprite.status = "dead"
        self.sprite.animation_speed = 0.10



    def update_health_bar(self, surface):
        # dessiner la bar de vie
        head = pygame.image.load('assets/head/head.png')

        surface.blit(head, (10, 20))

        pygame.draw.rect(
            surface,
            (60, 63, 60),
            [80, 70, self.max_health, 10],
        )
        pygame.draw.rect(
            surface,
            (111, 210, 46),
            [80, 70, self.current_health, 10],
        )

