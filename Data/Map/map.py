from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
from characters.entity import NPC
from projectile import Projectile


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list([pygame.Rect])
    ground: list([pygame.Rect])
    spade: list([pygame.Rect])
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list([Portal])
    npcs: list([NPC])


class MapManager:

    def __init__(self, screen, player, grec):
        self.maps = dict()
        self.screen = screen
        self.current_map = "carte"
        self.player = player
        self.grec = grec
        self.gravity = (0, 10)
        self.resistance = (0, 0)
        self.collision_sol = False

        self.register_map("carte", portals=[
            Portal(from_world="carte", origin_point="enter_carte2",
                   target_world="carte2", teleport_point="spawn_carte2")
        ], npcs=[
            NPC("grec", nb_points=2),
            NPC("greclance", nb_points=2)
        ])
        self.register_map("carte2", portals=[
            Portal(from_world="carte2", origin_point="enter_carte1",
                   target_world="carte", teleport_point="spawn_carte1")
        ])
        self.teleport_player("player")
        self.teleport_npcs()

    def check_spade_collision(self):
        if self.player.feet.collidelist(self.get_spade()) > -1:
            self.player.is_dead()

    # verification des types de collision en provenance de tiled
    def check_collision(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    self.grec.attack_player()
                    self.player.damage(self.grec.attack)
                else:
                    sprite.speed_walk = 1
                # if self.player.feet.colliderect(sprite.rect):
                #     sprite.damage_for_npc(self.player.attack_npc)
                # if sprite.current_health == 0:
                #     sprite.status = 'dead'

        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
            else:
                self.resistance = (0, 0)

        if self.player.feet.collidelist(self.get_ground()) > -1:
            self.resistance = (0, -10)
            self.collision_sol = True
            self.player.number_jump = 0
        else:
            self.resistance = (0, 0)

        if self.player.to_jump and self.collision_sol:
            if self.player.number_jump < 10:
                self.player.move_jump()

    def draw_collision(self):
        # for collision in self.get_ground():
        #     pygame.draw.rect(self.screen, (64, 64, 64, 0), collision)
        if self.player.sword:
            pygame.draw.rect(self.screen,  (64, 64, 64, 0), self.player.sword)
        # if self.player.sprite.head:
        #     pygame.draw.rect(self.screen,  (64, 64, 64, 0), self.player.sprite.head)

    # Gravite
    def gravity_game(self):
        self.player.position[1] += self.gravity[1] + self.resistance[1]

    # positionne mon joueur a la position choisie sur tiled
    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"tile/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())
        map_layer.zoom = 1.2

        # definir une liste qui va stocker mes collision
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height))

        ground = []

        for obj in tmx_data.objects:
            if obj.type == "sol":
                ground.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        spade = []

        for obj in tmx_data.objects:
            if obj.type == "kill":
                spade.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner ke groupe de calques
        group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=3)
        group.add(self.player)
        for npc in npcs:
            group.add(npc) 
        

        # creer un objet map
        self.maps[name] = Map(name, walls, ground, spade,
                              group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_ground(self):
        return self.get_map().ground

    def get_spade(self):
        return self.get_map().spade

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.position)
        self.player.update_health_bar(self.screen)
        self.grec.update_health_bar(self.screen)
        # self.draw_collision()
        # self.player.fireballs_rect(self.screen)

    def update(self):
        self.get_group().update()
        self.gravity_game()
        self.check_collision()
        self.check_spade_collision()
        for npc in self.get_map().npcs:
            npc.animate()
            npc.status = 'idle'
            npc.move()
