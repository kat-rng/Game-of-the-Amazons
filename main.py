# Practicing using pygame
import pygame

class Tile:

    def __init__(self, tile_array, x, y, x_bound, y_bound, state):
        # tile_array is an array of Tile objects. It should be provided by the TileManager
        self.tile_array = tile_array

        # Setting x and y location along with boundaries from initialization call parameters
        self.x = x
        self.y = y
        self.x_bound = x_bound
        self.y_bound = y_bound

        # Setting state variable, which describes how the tile should be displayed
        self.state = state


# START OF GAME CODE

# Initializes pygame
pygame.init()

# Creating a window
window = pygame.display.set_mode((500, 500))

# Adding a title to the window
pygame.display.set_caption("Practice game")

# Setting variables for displaying a rectangle
x = 50
y = 50
width = 40
height = 60

# Main game loop
run = True
while run:
    # Divide 1000 by the number below to get FPS estimate
    pygame.time.delay(100)

    # Event checker, reads through all recent events
    for event in pygame.event.get():
        # Checking if the game has been exited
        if event.type == pygame.QUIT:
            run = False

    # Displaying a rectangle
    pygame.draw.rect(window, (255, 0, 0), (x, y, width, height))

    # Updating the display
    pygame.display.update()

# Closes the window
pygame.quit()
