import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Définir les constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
SPRITE_ROWS = 4
SPRITE_COLUMNS = 4
PLAYER_SIZE = 64
PLAYER_SPEED = 3
MONSTER_SIZE = 64  # Remplacez 64 par la taille réelle des sprites de votre monstre

# Créer la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu avec des Sprites")

# Initialiser l'horloge
clock = pygame.time.Clock()

def game_over():
    # Afficher "Game Over" au centre de l'écran
    game_over_text = font.render("Game Over", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    
    # Afficher "Appuyez sur Entrée pour rejouer"
    restart_text = font.render("Appuyez sur Entrée pour rejouer", True, BLACK)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    
    # Attendre que le joueur appuie sur Entrée pour relancer le jeu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False  # Mettre waiting à False pour sortir de la boucle
                    return  # Ajouter un return pour sortir de la fonctions

# Charger la spritesheet du joueur (256x256 pixels)
player_spritesheet = pygame.image.load("player_spritesheet.png")
player_sprites_attack = pygame.image.load("attaque.png")

# Charger la police
font = pygame.font.Font(None, 36)

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

# Obtenir la liste de sprites d'attaque du joueur pour chaque direction
player_sprites_attack_up = get_sprites_from_spritesheet(player_sprites_attack, PLAYER_SIZE, 0)
player_sprites_attack_down = get_sprites_from_spritesheet(player_sprites_attack, PLAYER_SIZE, 1)
player_sprites_attack_left = get_sprites_from_spritesheet(player_sprites_attack, PLAYER_SIZE, 0)
player_sprites_attack_right = get_sprites_from_spritesheet(player_sprites_attack, PLAYER_SIZE, 1)

# Créer une classe pour la carte
class GameMap(pygame.sprite.Sprite):
    def __init__(self, map_image):
        super().__init__()
        self.image = pygame.image.load(map_image)
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.width, self.rect.height

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, map_width, map_height):
        super().__init__()
        self.direction = 'down'  # Direction initiale
        self.image_index = 0
        self.images = {
            'up': player_sprites_up,
            'down': player_sprites_down,
            'left': player_sprites_left,
            'right': player_sprites_right,
            'attack_up': player_sprites_attack_up,
            'attack_down': player_sprites_attack_down,
            'attack_left': player_sprites_attack_left,
            'attack_right': player_sprites_attack_right
        }
        self.image = self.images[self.direction][self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.map_width = map_width
        self.map_height = map_height
        self.map_rect = pygame.Rect(0, 0, map_width, map_height)  # Créer un rectangle pour représenter la carte
        self.attack_range = 120
        self.attacking = False
        self.attack_anim_frames = 4
        self.current_frame = 0
        self.health = 3  # Définir la santé initiale du joueur
        self.clock = pygame.time.Clock()  # Créer un objet Clock
        self.animation_speed = 0.2  # Vitesse de l'animation (plus la valeur est petite, plus l'animation est lente)
        self.frame_timer = 0
        self.frame_duration = 100  # Durée de chaque frame en millisecondes
        self.is_moving = False  # Indicateur pour savoir si le joueur est en mouvement
        self.attack_delay = 500  # Délai en millisecondes entre les attaques
        self.last_attack_time = 0  # Temps du dernier coup d'attaque
        
    def update(self, enemies):
         # Gérer le déplacement du joueur
        keys = pygame.key.get_pressed()
        if any(keys):
            self.move(keys)  # Nouvelle méthode pour gérer le déplacement
            camera.update(self)
            if keys[pygame.K_SPACE]:
                self.attack()  # Appel de la méthode d'attaque du joueur

        # Vérifier si une touche est enfoncée pour déterminer si le joueur est en mouvement
        keys = pygame.key.get_pressed()
        if any(keys):
            self.is_moving = True
            self.move(keys)  # Nouvelle méthode pour gérer le déplacement
            camera.update(self)
            if keys[pygame.K_SPACE]:
                self.attack()  # Appel de la méthode d'attaque du joueur
        else:
            self.is_moving = False

        # Animation : changer d'image pour créer une animation de marche ou d'attaque
        if self.is_moving:
            self.frame_timer += self.clock.tick()
            if self.frame_timer >= self.animation_speed * 1000:
                self.frame_timer = 0
                self.image_index = (self.image_index + 1) % len(self.images[self.direction])
                self.image = self.images[self.direction][self.image_index]

            # Vérifier si le joueur est en train d'attaquer
        if self.attacking:
            # Mettre à jour l'animation d'attaque
            self.attack_animation()


    def draw_health(self, screen):
        # Créez une surface de texte pour afficher les points de vie
        health_surface = font.render("Health: " + str(self.health), True, RED)
        # Obtenez le rectangle entourant la surface de texte
        health_rect = health_surface.get_rect()
        # Définissez la position du rectangle en haut à droite de l'écran
        health_rect.topright = (SCREEN_WIDTH - 10, 10)
        # Dessinez la surface de texte sur l'écran à la position spécifiée
        screen.blit(health_surface, health_rect)

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx -= PLAYER_SPEED
            self.direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += PLAYER_SPEED
            self.direction = 'right'
        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            dy -= PLAYER_SPEED
            self.direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += PLAYER_SPEED
            self.direction = 'down'

        new_rect = self.rect.move(dx, dy)
        if self.map_rect.contains(new_rect):
            self.rect = new_rect

    def attack(self):
        self.attacking = True
        self.image = self.images['attack_' + self.direction][0]  # Commencer l'animation d'attaque

    def handle_collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                dx = self.rect.centerx - enemy.rect.centerx
                dy = self.rect.centery - enemy.rect.centery
                length = max(1, math.hypot(dx, dy))
                dx /= length
                dy /= length

                self.rect.x += dx * PLAYER_SPEED
                self.rect.y += dy * PLAYER_SPEED

                if self.attacking:
                    enemy.hit()

    def take_damage(self, damage):
        self.health -= damage  # Réduire la santé du joueur en fonction des dégâts infligés
        # Vérifier si le joueur est mort
        if self.health <= 0:
            self.health = 0  # Assurez-vous que la santé ne devient pas négative
            # Déclencher le "Game Over"
            game_over()

    def attack_animation(self):
        # Vérifier si l'animation d'attaque est terminée
        if self.current_frame == self.attack_anim_frames - 1:
            self.attacking = False  # Arrêter l'attaque une fois l'animation terminée
            self.current_frame = 0  # Réinitialiser le compteur de frames d'attaque
            self.image = self.images[self.direction][self.image_index]  # Revenir à l'image normale du joueur
        else:
            # Mettre à jour l'image d'attaque pour l'animation
            self.frame_timer += self.clock.tick()
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame += 1
                self.image = self.images['attack_' + self.direction][self.current_frame]

# Charger la spritesheet du monstre (256x256 pixels)
monster_spritesheet = pygame.image.load("monster_spritesheet.png")
monster_sprites_attack = pygame.image.load("enemis_sprit_attaque.png")

# Obtenir la liste de sprites du monstre pour chaque direction
monster_sprites_up = get_sprites_from_spritesheet(monster_spritesheet, MONSTER_SIZE, 3)
monster_sprites_down = get_sprites_from_spritesheet(monster_spritesheet, MONSTER_SIZE, 0)
monster_sprites_left = get_sprites_from_spritesheet(monster_spritesheet, MONSTER_SIZE, 1)
monster_sprites_right = get_sprites_from_spritesheet(monster_spritesheet, MONSTER_SIZE, 2)

# Obtenir la liste de sprites d'attaque du monstre pour chaque direction
monster_sprites_attack_up = get_sprites_from_spritesheet(monster_sprites_attack, MONSTER_SIZE, 0)
monster_sprites_attack_down = get_sprites_from_spritesheet(monster_sprites_attack, MONSTER_SIZE, 1)
monster_sprites_attack_left = get_sprites_from_spritesheet(monster_sprites_attack, MONSTER_SIZE, 0)
monster_sprites_attack_right = get_sprites_from_spritesheet(monster_sprites_attack, MONSTER_SIZE, 1)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, attack_range):
        super().__init__()
        self.direction = 'down'  # Direction initiale
        self.image_index = 0
        self.images = {
            'up': monster_sprites_up,
            'down': monster_sprites_down,
            'left': monster_sprites_left,
            'right': monster_sprites_right,
            'attack_up': monster_sprites_attack_up,
            'attack_down': monster_sprites_attack_down,
            'attack_left': monster_sprites_attack_left,
            'attack_right': monster_sprites_attack_right
        }
        self.image = self.images[self.direction][self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.target = None  # Variable pour stocker la cible (le joueur)
        self.damage = 1  # Définir les dégâts infligés par l'ennemi
        self.attack_cooldown = 0  # Temps de recharge de l'attaque de l'ennemi
        self.attack_cooldown_duration = 3000  # Durée du cooldown en millisecondes (3 secondes)
        self.attack_range = attack_range  # Portée d'attaque de l'ennemi

    def update(self):
        dx, dy = 0, 0
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)

            if distance > 0:
                speed_factor = min(distance, self.speed) / distance
                self.rect.x += dx * speed_factor
                self.rect.y += dy * speed_factor

        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        if dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'
        self.image = self.images[self.direction][self.image_index]

        # Vérifier si le joueur est à portée d'attaque
        if self.is_in_attack_range():
            self.attack()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def set_target(self, target):
        self.target = target

    def is_in_attack_range(self):
        distance_to_player = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        return distance_to_player <= self.attack_range

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = self.attack_cooldown_duration
            self.image_index = 0
            self.image = self.images['attack_' + self.direction][self.image_index]  # Commencer l'animation d'attaque
            
            # Vérifier si le joueur est à portée d'attaque
            if self.is_in_attack_range():
                player.take_damage(self.damage)  # Infliger des dégâts au joueurd 

    def hit(self):
        self.kill()

# Création des ennemis avec une portée d'attaque spécifique
enemies = pygame.sprite.Group()
enemies.add(Enemy(200, 200, 2, 50))  # Passer l'argument attack_range

# Créer un groupe de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(enemies)
enemy_speed = 3  # Vitesse de déplacement de l'ennemi


# Créer la carte et le joueur, et les ajouter au groupe
game_map = GameMap("map.png")
player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, game_map.width, game_map.height)
all_sprites.add(game_map, player)

# Créer une classe pour la caméra
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + SCREEN_WIDTH // 2
        y = -target.rect.y + SCREEN_HEIGHT // 2

        # Empêcher la caméra de sortir des limites de la carte
        x = min(0, x)  # Ne pas aller à gauche de la carte
        y = min(0, y)  # Ne pas aller au-dessus de la carte
        x = max(-(self.width - SCREEN_WIDTH), x)  # Ne pas aller à droite de la carte
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Ne pas aller en dessous de la carte

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Créer une instance de la caméra
camera = Camera(game_map.rect.width, game_map.rect.height)

# Variable pour stocker le temps écoulé depuis la dernière apparition d'un ennemi
enemy_spawn_timer = 0
spawn_interval = 5 * 1000  # 5 secondes en millisecondes

# Boucle principale du jeu
while True:
    current_time = pygame.time.get_ticks()  # Obtenir le temps actuel en millisecondes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mettre à jour le joueur
    player.update(enemies)
    
    # Mettre à jour les ennemis
    for enemy in enemies:
        enemy.set_target(player)  # Définir le joueur comme cible de l'ennemi
        enemy.update()
    
    # Vérifier les collisions entre les ennemis
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
           player.handle_collision([enemy]) # Gérer la collision entre le joueur et l'ennemi
            

    # Vérifier si le joueur atteint la sortie de la carte
    if not game_map.rect.contains(player.rect):
        # Si le joueur sort de la carte, le ramener à l'intérieur
        player.rect.clamp_ip(game_map.rect)

    # Vérifier si le temps écoulé dépasse le délai d'apparition des ennemis
    if current_time - enemy_spawn_timer > spawn_interval:
        # Positions des coins de la carte
        corner_positions = [(0, 0), (game_map.rect.width - MONSTER_SIZE, 0), (0, game_map.rect.height - MONSTER_SIZE), (game_map.rect.width - MONSTER_SIZE, game_map.rect.height - MONSTER_SIZE)]
        
        # Créer un nouvel ennemi à chaque coin de la carte
        for position in corner_positions:
            new_enemy = Enemy(position[0], position[1], enemy_speed, 50)
            enemies.add(new_enemy)
            
        enemy_spawn_timer = current_time  # Réinitialiser le minuteur


    # Dessiner l'écran
    screen.fill(WHITE)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))  # Dessiner les autres sprites
    for enemy in enemies:
        # Dessiner l'ennemi uniquement s'il est à l'intérieur des limites de l'écran
        if camera.apply(enemy).colliderect(screen.get_rect()):
            screen.blit(enemy.image, camera.apply(enemy))  # Dessiner les ennemis

    player.draw_health(screen)  # Dessiner les points de vie après les autres sprites
    
    # Vérifier si le joueur est mort
    if player.health <= 0:
        game_over()  # Afficher l'écran de Game Over
        
        # Réinitialiser le joueur et les ennemis pour redémarrer le jeu
        player.health = 3
        for enemy in enemies:
            enemy.kill()
        player.rect.topleft = (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2)
        enemies.add(Enemy(0, SCREEN_HEIGHT, enemy_speed, 100))  # Réinitialiser les ennemis

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de rafraîchissement
    clock.tick(60)  # Ajuster la vitesse d'animation en changeant le nombre de ticks



