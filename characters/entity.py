
import random
import pygame

from characters.Player.Animatesprite.animatesprite import Animate_Sprite
from projectile import Projectile


class Entity(Animate_Sprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed_walk = 3
        self.speed_run = 5
        self.all_projectiles = pygame.sprite.Group()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.2, 12)
        # self.sword = pygame.Rect(0, 0, 10, 10)
        self.old_position = self.position.copy()
        self.jump = 0
        self.jump_high = 0
        self.jump_down = 5
        self.number_jump = 0
        self.to_jump = False

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.facing_right = True
        self.position[0] += self.speed_walk
        self.status = 'run'
        self.animation_speed = 0.25

    def move_left(self):
        self.facing_right = False
        self.position[0] -= self.speed_walk
        # self.moves()
        self.status = 'run'
        self.animation_speed = 0.25

    def move_right_npc(self):
        self.facing_right = True
        self.position[0] += self.speed_walk
        self.status = 'run'
        self.animation_speed = 0.25

    def move_left_npc(self):
        self.facing_right = False
        self.position[0] -= self.speed_walk
        self.status = 'run'
        self.animation_speed = 0.25

    def run_right(self):
        self.position[0] += self.speed_run
        self.status = 'run'
        self.animation_speed = 0.25

    def run_left(self):
        self.position[0] -= self.speed_run
        self.status = 'run'
        self.animation_speed = 0.25

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        # self.sword.center = self.rect.center
        self.position[0] = self.rect.x
        self.position[1] = self.rect.y

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position.copy()
        self.feet.midbottom = self.rect.midbottom
        self.update()

    def move_jump(self):
        if self.to_jump:
            if self.jump_high >= 8:
                self.jump_down -= 1
                self.jump = self.jump_down
                self.status = 'jump'
                self.animation_speed = 0.3

            else:
                self.jump_high += 1
                self.jump = self.jump_high
                self.status = 'jump'
                self.animation_speed = 0.3

            if self.jump_down < 0:
                self.jump_high = 0
                self.jump_down = 5
                self.to_jump = False
                self.status = 'idle'
        self.position[1] = self.position[1] - (10 * (self.jump / 2))

    def collision_top_screen(self):
        if self.position[1] > 0:
            self.position[1] = 0


class Player(Entity):

    def __init__(self, camera):
        super().__init__("PLAYER", 0, 0)
        self.current_health = 100
        self.max_health = 100
        self.attack_npc = 5
        self.last_update_time = pygame.time.get_ticks()
        self.camera = camera

    def is_dead(self):
        self.current_health = 0
        if self.current_health == 0:
            self.status = "dead"
            self.animation_speed = 0.10

    def attack(self):
        self.status = 'attack'

    def damage(self, amount):
        if self.current_health - amount > amount:
            self.current_health -= amount
        else:
            self.current_health = 0
            self.status = 'dead'

    def update_health_bar(self, surface):
        # dessiner la bar de vie
        head = pygame.image.load('assets/head/head.png')
        deadHead = pygame.image.load('assets/head/dead__head.png')

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

        if self.current_health < 30:
            surface.blit(deadHead, (10, 20))
        else:
            surface.blit(head, (10, 20))

        current_time = pygame.time.get_ticks()  # Obtenir le temps actuel
        if current_time - self.last_update_time > 5000:  # Vérifier si 3 secondes se sont écoulées
            if self.current_health < 50:
                self.current_health += 5
            self.last_update_time = current_time

    def launch_projectile(self, camera):
        # creer une nouvel instance de la classe projectile
        self.all_projectiles.add(Projectile(self, camera, self.facing_right))
        self.status = 'attack'
        self.animation_speed = 0.15

    # def fireballs_rect(self, screen):
    #     for projectile in self.all_projectiles:
    #         projectile.draw_fireballs(screen)


class NPC(Entity):

    def __init__(self, name, nb_points):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        # self.dialog = dialog
        self.current_health = 100
        self.points = []
        self.name = name
        self.speed_walk = random.randint(1, 3)
        self.current_point = 0

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left_npc()

        if current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right_npc()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def damage_for_npc(self, amount):
        # infliger les degat
        self.current_health -= amount

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


class Grec(NPC):
    def __init__(self, camera):
        super().__init__("grec", 2)
        self.current_health = 100
        self.max_health = 100
        self.attack = 0.5
        self.camera = camera

    def update_health_bar(self, surface):
        # dessiner la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [
                         100, self.position[1], self.max_health, 10])
        pygame.draw.rect(surface, (220, 20, 60), [
                         100, self.position[1], self.current_health, 10])

    def is_dead(self):
        self.status = 'dead'
        self.animation_speed = 0.10

    def attack_player(self):
        self.speed_walk = 0
        if self.speed_walk >= 0:
            self.status = 'attack'
