import pygame
import sys
from classes import Game, Player
from Chateau import ChateauGame, PlayerChateau

# Initialisation de Pygame
pygame.init()

# Définir les constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
PLAYER_SIZE = 64
PLAYER_SPEED = 5
FRAME_WIDTH = 64  # Largeur d'une frame du joueur
TELEPORT_THRESHOLD = 10  # Seuil de téléportation (distance autorisée pour le téléport)

# Créer la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu avec des Sprites")


# Créer une classe pour la carte
class GameMap(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()


#global player,map_image,map_rect,game_map,SCREEN_WIDTH,SCREEN_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT,PLAYER_SPEED,GRAVITY,JUMP_SPEED,chateau_image,chateau_rect,scale_factor,player_x,player_y,player_dx,player_dy,chateau_x, player_index,player_frames, player_spritesheet

class MainGame(Game):
    def __init__(self, screen, clock, width, height):
        super().__init__(screen, clock, width, height)
        # Charger l'image de la carte
        self.map_image = pygame.image.load("map.jpg")
        self.map_rect = self.map_image.get_rect()  # Rectangle délimitant la carte

        # Créer les sprites
        self.game_map = GameMap(self.map_image)
        self.player = Player(self.map_rect)

        # Créer un groupe de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.game_map, self.player)  # Ajouter la carte dans le groupe

    def game_update(self):
        self.player.update()

        # Centre la caméra sur le joueur
        self.camera_x = max(0, min(self.player.rect.x - self.SCREEN_WIDTH // 2, self.map_rect.width - self.SCREEN_WIDTH))
        self.camera_y = max(0, min(self.player.rect.y - self.SCREEN_HEIGHT // 2, self.map_rect.height - self.SCREEN_HEIGHT))

        # Dessiner l'écran
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.game_map.image, (0 - self.camera_x, 0 - self.camera_y))
        self.screen.blit(self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y - self.camera_y))

        pygame.display.flip()
        self.clock.tick(60)

clock = pygame.time.Clock()
main_game=MainGame(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
chateau_game=ChateauGame(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
#chateau_game=Game(chateau_map,init_chateaumap, screen, clock)
actual_game=main_game

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP0:
                print("main")
                actual_game=main_game
            if event.key == pygame.K_KP1:
                print("chateau")
                actual_game=chateau_game
    actual_game.game_update()

 
pygame.quit()
sys.exit()

