import pygame, sys

from maze_generator import *
from level import Level
from Display import *

# level: size_map, cell_width, wall_width
ATRIBUTES = {'Easy' : (20, 42, 8), 'Medium' : (40, 22, 5), 'Hard' : (100, 7, 1)}

class Game:
    def __init__(self, screen, mode_play, difficult, start_x, start_y, end_x, end_y, time, step, game_name, username, maze=None, status=None, volume=1):
        # general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Load images
        self.img_ground = pygame.image.load('assets/tilemap/ground.png')
        self.img_bg = pygame.image.load('assets/tilemap/background.png')
        self.img_border = pygame.image.load('assets/tilemap/border.png')
        self.display_surface = pygame.surface.Surface((688, 688))

        # Setup game settings
        self.mode_play = mode_play
        self.difficult = difficult
        self.game_name = game_name
        self.username = username
        self.step = step
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        
        # Sound setup
        self.sound = pygame.mixer.Sound('sound/select sound.mp3')
        self.sound.set_volume(volume)
        self.volume = volume

        # Maze setup
        if maze is None:
            self.maze = Maze(self.display_surface, ATRIBUTES[difficult][0], start_x, start_y, end_x, end_y, ATRIBUTES[difficult][1], ATRIBUTES[difficult][2])
            self.maze.mazeGenerate()
        else:
            self.maze = Maze(self.display_surface, ATRIBUTES[difficult][0], start_x, start_y, end_x, end_y, ATRIBUTES[difficult][1], ATRIBUTES[difficult][2], maze)

        # Level setup
        if status is None:
            self.level = Level(self, int(self.maze.width - 2 * self.maze.wall_width))
        else:
            self.level = Level(self, int(self.maze.width - 2 * self.maze.wall_width), status)

        # Menu setup, now includes 'home'
        self.menu = Display(self.screen, { 
                            'new' : ((970, 589), volume), 
                            'help' : ((1100, 589), volume),
                            'home' : ((860, 589), volume)  # new home button
                        },
                        [(f'Name: {game_name}', (860, 300)), 
                         (f'Difficult: {difficult}', (860, 360)), 
                         (f'Mode: {mode_play}', (860, 420)), 
                         ('Time: 00:00', (860, 480))])
        self.menu.clock.get(time)

    def run(self):
        running = True
        if self.mode_play in ('Auto (A*)', 'Auto (BFS)'):
            self.level.getAuto(self.mode_play)

        while running:
            self.display_surface.blit(self.img_ground, (0, 0))
            self.level.run()

            # Blit images
            self.screen.blit(self.img_bg, (0, 0))
            self.screen.blit(self.display_surface, (39, 33))
            self.screen.blit(self.img_border, (0, 0))

            # Check menu status
            status = self.menu.render(self.level.pause_sound)
            if status == 'new':
                # Reset level
                self.maze.reset()
                self.maze.mazeGenerate()
                self.level = Level(self, int(self.maze.width - 2 * self.maze.wall_width))
                self.menu.reset_time()
                self.step = 0
                if self.mode_play in ('Auto (A*)', 'Auto (BFS)'):
                    self.level.getAuto(self.mode_play)
            elif status == 'help':
                # Display help screen
                img = pygame.image.load('assets/help_game.png')
                running_help = True
                while running_help:
                    self.screen.blit(img, (0, 0))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running_help = False
                    pygame.display.update()
                    self.clock.tick(60)
            elif status == 'home':
                # Return to home screen
                running = False  # Exit game loop to return to main screen

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h and self.mode_play not in ('Auto (A*)', 'Auto (BFS)'):
                        self.sound.play()
                        self.level.player.getHint()
                    if event.key == pygame.K_r and self.mode_play in ('Auto (A*)', 'Auto (BFS)') and len(self.level.visited) > 0:
                        self.sound.play()
                        # Switch mode between A* and BFS
                        self.mode_play = 'Auto (BFS)' if self.mode_play == 'Auto (A*)' else 'Auto (A*)'
                        self.menu.text_boxes[2].update(f'Mode: {self.mode_play}')
                        self.level.getAuto(self.mode_play)

            pygame.display.update()
            self.clock.tick(60)
