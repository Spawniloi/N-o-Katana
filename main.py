from classes import Game, Player

# Utilisation de la classe Game
game = Game(800, 600)
player = Player(game.screen_width / 2 , game.screen_height / 2, 1000, 1000, game.sprite_group)
game.run_game() 
