import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Définir les constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
SPRITESHEET_SIZE = 256
SPRITE_ROWS = 4
SPRITE_COLUMNS = 4
PLAYER_SIZE = 64
PLAYER_SPEED = 5  # Réduit la vitesse pour éviter que le joueur ne dépasse les limites trop rapidement

# Créer la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu avec des Sprites")

# Charger la spritesheet du joueur (256x256 pixels)
player_spritesheet = pygame.image.load("player_spritesheet.png")

# Charger les images de la carte
map_images = {
    "map": pygame.transform.scale(pygame.image.load("map.jpg"), (736, 736)),
    "map_boss": pygame.transform.scale(pygame.image.load("map_boss.jpg"), (736, 736))
}

# Fonction pour découper une spritesheet en une liste d'images
def get_sprites_from_spritesheet(spritesheet, sprite_size, row):
    sprites = []
    sheet_width, sheet_height = spritesheet.get_size()
    
    for col in range(SPRITE_COLUMNS):
        x = col * sprite_size
        y = row * sprite_size
        sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_size, sprite_size))
        sprites.append(sprite)
    return sprites

# Obtenir la liste de sprites du joueur pour chaque direction
player_sprites_up = get_sprites_from_spritesheet(player_spritesheet, PLAYER_SIZE, 3)
player_sprites_down = get_sprites_from_spritesheet(player_spritesheet, PLAYER_SIZE, 0)
player_sprites_left = get_sprites_from_spritesheet(player_spritesheet, PLAYER_SIZE, 1)
player_sprites_right = get_sprites_from_spritesheet(player_spritesheet, PLAYER_SIZE, 2)

# Créer une classe pour la carte
class GameMap(pygame.sprite.Sprite):
    def __init__(self, map_image):
        super().__init__()
        self.image = map_image
        self.rect = self.image.get_rect()

# Créer une classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = 'down'  # Direction initiale
        self.image_index = 0
        self.images = {
            'up': player_sprites_up,
            'down': player_sprites_down,
            'left': player_sprites_left,
            'right': player_sprites_right
        }
        self.image = self.images[self.direction][self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, map_rect):
        global current_map  # Utiliser la variable globale current_map

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_q] or keys[pygame.K_a]:
            dx -= PLAYER_SPEED
            self.direction = 'left'
        elif keys[pygame.K_d]:
            dx += PLAYER_SPEED
            self.direction = 'right'
        elif keys[pygame.K_z] or keys[pygame.K_w]:
            dy -= PLAYER_SPEED
            self.direction = 'up'
        elif keys[pygame.K_s]:
            dy += PLAYER_SPEED
            self.direction = 'down'

        # Animation : changer d'image pour créer une animation de marche
        self.image_index = (self.image_index + 1) % len(self.images[self.direction])
        self.image = self.images[self.direction][self.image_index]

        # Vérifier les collisions avec les bords de la carte
        if self.rect.left + dx >= 0 and self.rect.right + dx <= map_rect.width:
            self.rect.x += dx
        if self.rect.top + dy >= 0 and self.rect.bottom + dy <= map_rect.height:
            self.rect.y += dy

        # Gérer la collision avec les portails (par exemple, des rectangles aux coins)
        if self.rect.colliderect(map_rect["top_left_portal"]) or self.rect.colliderect(map_rect["bottom_portal"]):
            # Changer de carte et repositionner le joueur
            if current_map == "map":
                self.rect.x, self.rect.y = map_rect["map_boss_player_position"]  # Repositionner le joueur sur la nouvelle carte
                current_map = "map_boss"  # Changer la carte actuelle en "map_boss"
            elif current_map == "map_boss":
                self.rect.x, self.rect.y = map_rect["map_player_position"]  # Repositionner le joueur sur la première carte
                current_map = "map"  # Changer la carte actuelle en "map"
        return current_map  # Retourner la carte actuelle si aucun changement n'est nécessaire

# Créer un groupe de sprites
all_sprites = pygame.sprite.Group()

# Créer la carte et le joueur, et les ajouter au groupe
current_map = "map"  # Définir la carte initiale
game_map = GameMap(map_images[current_map])
player = Player(50, 50)  # Position initiale du joueur
all_sprites.add(game_map, player)

# Définir les coordonnées des portails aux coins de la carte
map_rect = {
    "top_left_portal": pygame.Rect(0, 0, 50, 50),
    "bottom_portal": pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50, 50, 50),
    "map_boss_player_position": (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, 100),  # Position du joueur sur la carte boss
    "map_player_position": (50, 50)  # Position du joueur sur la première carte
}

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mettre à jour le joueur
    keys = pygame.key.get_pressed()
    if any(keys):
        current_map = player.update(game_map.rect)

    # Dessiner l'écran
    screen.fill(WHITE)
    screen.blit(game_map.image, game_map.rect)  # Dessiner la carte
    screen.blit(player.image, player.rect)  # Dessiner le joueur

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de rafraîchissement
    pygame.time.Clock().tick(60)  # Ajuster la vitesse d'animation en changeant le nombre de ticks
