
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
        PLAYER_SIZE = 64
        PLAYER_SPEED = 5
        FRAME_WIDTH = 64  # Largeur d'une frame du joueur
        # Charger l'image du joueur
        player_spritesheet = pygame.image.load("player_spritesheet.png")
        # Découper les frames du joueur en 4 colonnes de 64 pixels
        player_frames = [player_spritesheet.subsurface((i * FRAME_WIDTH, 0, FRAME_WIDTH, PLAYER_SIZE)) for i in range(4)]
        self.frames = player_frames
        self.index = 0  # Index de la frame actuelle
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(map_rect.width // 2, map_rect.height // 2))  # Centrer le joueur sur la carte
        self.map_rect = map_rect  # Rectangle délimitant la carte

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_q]) * PLAYER_SPEED
        dy = (keys[pygame.K_s] - keys[pygame.K_z]) * PLAYER_SPEED

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Vérifier que le joueur ne dépasse pas la carte
        if 0 <= new_x <= self.map_rect.width - PLAYER_SIZE and 0 <= new_y <= self.map_rect.height - PLAYER_SIZE:
            self.rect.x = new_x
            self.rect.y = new_y

            # Afficher les coordonnées de déplacement dans la console
            # print(f"Coordonnées de déplacement : ({self.rect.x}, {self.rect.y})")

            # Vérifier si le joueur est près des coordonnées de téléportation
            if self.rect.collidepoint(23, 383) and keys[pygame.K_RETURN]:
                pass
                # Téléporter le personnage vers une autre image
                # self.game_map.image = pygame.image.load("map_boss.jpg")
                # Placer le personnage à une nouvelle position sur la nouvelle carte
                # self.rect.topleft = (100, 100)  # Coordonnées de téléportation sur la nouvelle carte

# Vérifier si le joueur est près des coordonnées de téléportation
            if self.rect.collidepoint(336, 316) and keys[pygame.K_RETURN]:
                pass
                # Téléporter le personnage vers une autre image
                # self.game_map.image = pygame.image.load("Chateau.png")
                # Placer le personnage à une nouvelle position sur la nouvelle carte
                # self.rect.topleft = (100, 100)  # Coordonnées de téléportation sur la nouvelle carte


