import pygame
import sys
from classes import Map, Player

class PlayerChateau(Player):
    def update(self):
        pass

# Définir les constantes

class ChateauGame (Map):

    def __init__(self, screen, clock, width, height):
        super().__init__(screen, clock, width, height)
        print("init")
        self.PLAYER_WIDTH, self.PLAYER_HEIGHT = 64, 64
        self.PLAYER_SPEED = 5
        self.GRAVITY = 0.5
        self.JUMP_SPEED = -10

        # Charger l'image du château
        self.chateau_image = pygame.image.load("chateau.png")
        self.chateau_rect =  self.chateau_image.get_rect()
        # Redimensionner l'image du château pour qu'elle remplisse la hauteur de l'écran
        scale_factor = self.SCREEN_HEIGHT / self.chateau_rect.height
        self.chateau_image = pygame.transform.scale( self.chateau_image, (int(self.chateau_rect.width * scale_factor), self.SCREEN_HEIGHT))
        self.chateau_rect =  self.chateau_image.get_rect()

        # Position initiale du joueur
        self.player_x = self.SCREEN_WIDTH // 2
        self.player_y = self.SCREEN_HEIGHT - self.PLAYER_HEIGHT
        self.player_dx, self.player_dy = 0, 0  # Vitesse horizontale et verticale du joueur

        # Position initiale du décor
        self.chateau_x = 0
        self.player_index = 0
        self.player_spritesheet = pygame.image.load("player_spritesheet.png")
        self.player_frames = [self.player_spritesheet.subsurface((i * self.PLAYER_WIDTH, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)) for i in range(4)]

    # Charger l'image du joueur
    #player_spritesheet = pygame.image.load("player_spritesheet.png")
    #player_frames = [player_spritesheet.subsurface((i * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(4)]
    #player_rect = player_frames[0].get_rect(bottomleft=(player_x, player_y))
    #player_index = 0

    def game_update(self):

        keys = pygame.key.get_pressed()

        # Saut du joueur
    # Saut du joueur
        if keys[pygame.K_SPACE] and self.player_dy == 0:  # Vérifie si le joueur est au sol (sa vitesse verticale est nulle)
            self.player_dy = self.JUMP_SPEED

        # Déplacer le joueur
        if keys[pygame.K_q]:
            self.self.player_dx = -self.PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.player_dx = self.PLAYER_SPEED
        else:
            self.player_dx = 0

        # Appliquer la gravité
        self.player_dy +=  self.GRAVITY
        self.player_y += self.player_dy

        # Empêcher le joueur de sortir de l'écran en vertical
        if self.player_y > self.SCREEN_HEIGHT - self.PLAYER_HEIGHT:
            self.player_y = self.SCREEN_HEIGHT - self.PLAYER_HEIGHT
            self.player_dy = 0

        # Empêcher le joueur de sortir de l'écran en horizontal
        self.player_x += self.player_dx
        if self.player_x < 0:
            self.player_x = 0
        elif self.player_x > self.SCREEN_WIDTH - self.PLAYER_WIDTH:
            self.player_x = self.SCREEN_WIDTH - self.PLAYER_WIDTH

        # Animation du joueur
        self.player_index = (self.player_index + 1) % 4
        player_image = self.player_frames[self.player_index]

        # Déplacer le décor
        self.chateau_x -= self.player_dx

        # Si le décor dépasse l'écran, réinitialiser sa position
        if self.chateau_x < -self.chateau_rect.width:
            self.chateau_x = 0

        # Dessiner l'écran
        self.screen.fill((255, 255, 255))
        self.screen.blit( self.chateau_image, (self.chateau_x, 0))

        # Calculer la position de la caméra pour centrer le joueur
        camera_x = self.player_x - self.SCREEN_WIDTH // 2
        camera_x = max(0, min(camera_x, self.chateau_rect.width - self.SCREEN_WIDTH))

        # Afficher le joueur centré sur la caméra
        self.screen.blit(player_image, (self.player_x - camera_x, self.player_y))

        # Mettre à jour l'affichage
        pygame.display.flip()
        self.clock.tick(60)  # Limiter la vitesse de l'animation du personnage pour la clarté visuelle et le mouvement
