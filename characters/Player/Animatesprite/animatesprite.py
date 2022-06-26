import pygame
from Data.Support_Animation.support import import_folder


class Animate_Sprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.character_path = f'assets/{name}/'
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.25
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect()

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.image.set_colorkey([0, 0, 0])
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 12)
        # self.head = pygame.Rect(0, 0, self.rect.width * 0.5, 12)


    # def get_image(self, x, y):
    #     image = pygame.Surface([138, 138])
    #     image.blit(self.sprite, (0, 0), (x, y, 138, 138))
    #     return image

    def import_character_assets(self):
        self.character_path
        self.animations = {'idle': [], 'run': [], 'roll': [],
                           'jump': [], 'fall': [], 'attack': [], 'spattack': [], 'dead': []}

        for animation in self.animations.keys():
            full_path = self.character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
        else:
            self.facing_right = False
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(
                bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def getstatus(self):
        self.status

    def get_rect(self):
        return self.rect
