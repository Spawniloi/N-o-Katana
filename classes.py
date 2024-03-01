import pygame

# Fonction pour découper une spritesheet en une liste d'images
def get_sprites_from_spritesheet(spritesheet, sprite_size, row, columns):
    sprites = []
    sheet_width, sheet_height = spritesheet.get_size()
    
    for col in range(columns):
        x = col * sprite_size
        y = row * sprite_size
        sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_size, sprite_size))
        sprites.append(sprite)
    return sprites

class Game :
    def __init__(self, width, height):
        print("init")
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Néon-Katana")
        self.clock = pygame.time.Clock()
        self.sprite_group = pygame.sprite.Group()
   
    def draw (self) :
        print("draw")
        # Effacer l'écran avec une couleur de fond
        self.screen.fill((0, 0, 0))

        # Dessiner d'autres éléments du jeu ici, tels que des sprites, des textes, etc.
        self.sprite_group.draw(self.screen)
        # Mettre à jour l'affichage pour montrer les changements
        pygame.display.flip()

    def update (self) :
        print("update")
        self.sprite_group.update()
        # Mettre à jour la logique du jeu ici, telle que la mise à jour des positions des sprites, la gestion des collisions, etc.

    def loop (self) :
        print("loop")
            #event
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.draw()

    def run_game(self):
        self.loop()
            # Autres mises à jour et rendus du jeu ici

        pygame.quit()  

class Map :
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
    def __init__(self, x, y, map_width, map_height, group):
        super().__init__(group)
        self.direction = 'down'  # Direction initiale
        self.image_index = 0
        player_spritesheet = pygame.image.load("player_spritesheet.png")
        player_sprites_attack = pygame.image.load("attaque.png")
        self.size = 64
        # Obtenir la liste de sprites du joueur pour chaque direction
        player_sprites_up = get_sprites_from_spritesheet(player_spritesheet, self.size, 3, 4)
        player_sprites_down = get_sprites_from_spritesheet(player_spritesheet, self.size, 0, 4)
        player_sprites_left = get_sprites_from_spritesheet(player_spritesheet, self.size, 1, 4)
        player_sprites_right = get_sprites_from_spritesheet(player_spritesheet, self.size, 2, 4)

        # Obtenir la liste de sprites d'attaque du joueur pour chaque direction
        player_sprites_attack_up = get_sprites_from_spritesheet(player_spritesheet, self.size, 0, 4)
        player_sprites_attack_down = get_sprites_from_spritesheet(player_spritesheet, self.size, 3, 4)
        player_sprites_attack_left = get_sprites_from_spritesheet(player_spritesheet, self.size, 2, 4)
        player_sprites_attack_right = get_sprites_from_spritesheet(player_spritesheet, self.size, 1, 4)
        self.speed = 3
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
        self.rect = self.image.get_rect(topleft=(x -self.size, y-self.size))
        self.map_width = map_width
        self.map_height = map_height
        self.map_rect = pygame.Rect(0, 0, map_width, map_height)  # Créer un rectangle pour représenter la carte
        self.attack_range = 150
        self.attacking = False
        self.attack_anim_frames = 4
        self.current_frame = 0
        self.health = 3  # Définir la santé initiale du joueur
        self.animation_speed = 0.2  # Vitesse de l'animation (plus la valeur est petite, plus l'animation est lente)
        self.frame_timer = 0
        self.frame_duration = 100  # Durée de chaque frame en millisecondes
        self.is_moving = False  # Indicateur pour savoir si le joueur est en mouvement
        
        
    def update(self):
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

    def draw_health(self, screen):
        # Créez une surface de texte pour afficher les points de vie
        health_surface = font.render("Health: " + str(self.health), True, RED)
        # Obtenez le rectangle entourant la surface de texte
        health_rect = health_surface.get_rect()
        # Définissez la position du rectangle en haut à droite de l'écran
        # health_rect.topright = (SCREEN_WIDTH - 10, 10)
        # Dessinez la surface de texte sur l'écran à la position spécifiée
        screen.blit(health_surface, health_rect)

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx -= self.speed 
            self.direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed 
            self.direction = 'right'
        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            dy -= self.speed 
            self.direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed 
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

                self.rect.x += dx * self.speed 
                self.rect.y += dy * self.speed 

                if self.attacking:
                    enemy.hit()

    def take_damage(self, damage):
        self.health -= damage  # Réduire la santé du joueur en fonction des dégâts infligés
        # Vérifier si le joueur est mort
        if self.health <= 0:
            self.health = 0  # Assurez-vous que la santé ne devient pas négative
            # Déclencher le "Game Over"
            game_over()
class TeleportZone:
    def __init__(self, x, y, width, height, destination_image, destination_position):
        self.rect = pygame.Rect(x, y, width, height)
        self.destination_image = destination_image
        self.destination_position = destination_position

    def check_collision_and_teleport(self, player_rect, keys):
        if player_rect.colliderect(self.rect) and keys[pygame.K_RETURN]:
            return True
        return False
