import pygame
from Data.Map.map import MapManager
from characters.entity import NPC, Grec, Player
from Data.Camera.camera import Camera


class Game:

    def __init__(self, screen):
        self.is_playing = False
        # creation de la fenetre du jeu
        self.screen = screen
        self.screen_width = 1280  # Ajoutez la largeur de l'écran
        self.screen_height = 720  # Ajoutez la hauteur de l'écran
        self.level_width = 5000  # Ajoutez la largeur du niveau
        self.level_height = 720  # Ajoutez la hauteur du niveau
        self.font = pygame.font.Font('freesansbold.ttf', 55)
        # generer un joueur
        self.npc = NPC("grec", 2)
        self.player = Player(Camera)
        self.grec = Grec(Camera)
        self.map_manager = MapManager(self.screen, self.player, self.grec)
        # creer lobjet camera
        self.camera = Camera(self.player, self.screen_width,
                             self.screen_height, self.level_width, self.level_height)

        self.pressed = {}

    def player_dead(self):
        if self.player.current_health == 0:
            self.game_over()

    def start(self):
        self.is_playing = True

    def restart_game(self):
        self.is_playing = True
        self.map_manager.update()
        self.map_manager.teleport_player("player")
        self.player.status = 'idle'
        self.player.current_health = self.player.max_health

    def game_over_text(self):
        over_text = self.font.render("GAME OVER", True, (64, 64, 64))
        self.screen.blit(over_text, (580, 200))

    def game_over(self):
        # remettre le jeu a neuf, retirer les mponstre remmetre le joueur a 100 point de vie , jeu en attente
        self.map_manager.update()
        self.map_manager.teleport_player("player")
        self.player.status = 'idle'
        self.player.current_health = self.player.max_health
        self.is_playing = False

    def move(self):
        if self.pressed.get(pygame.K_ESCAPE):
            self.is_playing = False
        if self.pressed.get(pygame.K_RIGHT):
            self.player.move_right()
        if self.pressed.get(pygame.K_d):
            self.player.move_right()
        if self.pressed.get(pygame.K_LEFT):
            self.player.move_left()
        if self.pressed.get(pygame.K_q):
            self.player.move_left()
        if self.pressed.get(pygame.K_UP) and self.player.position[1] > 0:
            self.player.to_jump = True
            self.player.number_jump += 1
        if self.pressed.get(pygame.K_z) and self.player.position[1] > 0:
            self.player.to_jump = True
            self.player.number_jump += 1
        if self.pressed.get(pygame.K_RIGHT) and self.pressed.get(pygame.K_LSHIFT):
            self.player.run_right()
        if self.pressed.get(pygame.K_LEFT) and self.pressed.get(pygame.K_LSHIFT):
            self.player.run_left()
        if self.pressed.get(pygame.K_d) and self.pressed.get(pygame.K_LSHIFT):
            self.player.run_right()
        if self.pressed.get(pygame.K_q) and self.pressed.get(pygame.K_LSHIFT):
            self.player.run_left()
        if self.pressed.get(pygame.K_SPACE):
            self.player.attack()
            self.player.animation_speed = 0.23
        # if self.pressed.get(pygame.K_LCTRL):
        #     self.player.launch_projectile()

    def update(self):
        self.map_manager.update()
        self.camera.update()
        self.player.save_location()
        self.move()
        self.map_manager.draw()
        self.player.animate()
        self.player_dead()
        for projectile in self.player.all_projectiles:
            projectile.move()
        self.player.all_projectiles.draw(self.screen)
