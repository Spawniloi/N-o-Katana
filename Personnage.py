import pygame
class Game :
    def __init__(self, screen, clock, width, height):
        self.screen = screen
        self.clock= clock
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT =height
    def game_update (self):
        pass
    def init_game (self):
        pass

# Créer une classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, map_rect):
        super().__init__()
        self.PLAYER_SIZE = 64
        self.PLAYER_SPEED = 5
        self.FRAME_WIDTH = 64  # Largeur d'une frame du joueur
        self.on_map_change = []
        # Charger l'image du joueur
        player_spritesheet = pygame.image.load("player_spritesheet.png")
        # Découper les frames du joueur en 4 colonnes de 64 pixels
        player_frames = [player_spritesheet.subsurface((i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.PLAYER_SIZE)) for i in range(4)]
        self.frames = player_frames
        self.index = 0  # Index de la frame actuelle
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(map_rect.width // 2, map_rect.height // 2))  # Centrer le joueur sur la carte
        self.map_rect = map_rect  # Rectangle délimitant la carte

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_q]) * self.PLAYER_SPEED
        dy = (keys[pygame.K_s] - keys[pygame.K_z]) * self.PLAYER_SPEED

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Vérifier que le joueur ne dépasse pas la carte
        if 0 <= new_x <= self.map_rect.width - self.PLAYER_SIZE and 0 <= new_y <= self.map_rect.height - self.PLAYER_SIZE:
            self.rect.x = new_x
            self.rect.y = new_y
        
    def map_change(self):
        for event in self.on_map_change:
            event()

class TeleportZone:
    def __init__(self, x, y, width, height, destination_image, destination_position):
        self.rect = pygame.Rect(x, y, width, height)
        self.destination_image = destination_image
        self.destination_position = destination_position

    def check_collision_and_teleport(self, player_rect, keys):
        if player_rect.colliderect(self.rect) and keys[pygame.K_RETURN]:
            return True
        return False









