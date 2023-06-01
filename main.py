# Practicing using pygame
import pygame
import numpy as np


class Tile:
    # The core game logic element
    # Defines what each tile should be displayed as through the state variable
    # Controls the core game logic through its various functions
    # Frequently uses "recursive" calls via the tile_array

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


    def propagate(self, offset_x, offset_y, is_considering_movement):
        # Used to display potential movement locations when requested.
        # is_considering is used to determine behavior later regarding changing state and continuing to propagate
        # (see state section in __init__ for more info on why the state checks are structured as they are later)

        if is_considering_movement & self.state == 0:
            # If considering movement and the tile is empty, then switch to showing that the tile can be accessed
            self.state = 1
        elif ~is_considering_movement & self.state == 1:
            # If considering movement and the tile is empty, then switch to showing that the tile can be accessed
            self.state = 0
        else:
            # No changes are needed, so end this recursive call
            return

        # Finding the next tile location from the given offset
        next_x = self.x + offset_x
        next_y = self.y + offset_y

        if (next_x >= 0 & next_x < self.x_bound) & (next_y >= 0 & next_y < self.y_bound):
            self.tile_array[next_x, next_y].propogate(self.x, self.y)



class TileManager:
    # The container (indirectly) for all the Tiles
    # Manages communication between the game interface and the Tile elements
    # Generates the tile_array and sends it to each tile element

    def __init__(self, side_length = 10):
        # Setting up a square board
        self.x_length = side_length
        self.y_length = side_length

        # Creating an empty tile array
        self.tile_array = np.zeros((self.x_length, self.y_length), dtype=Tile)
        
        # Loop to fill in all the locations inside tile_array
        for x in range(self.x_length):
            for y in range(self.y_length):
                self.tile_array[x, y] = Tile(self.tile_array, x, y, self.x_length, self.y_length, 0)

# START OF GAME CODE

# Initializes pygame
pygame.init()

# Creating a window
window = pygame.display.set_mode((500, 500))

# Adding a title to the window
pygame.display.set_caption("Practice game")

# Setting variables for displaying a rectangle
x_location = 50
y_location = 50
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
    pygame.draw.rect(window, (255, 0, 0), (x_location, y_location, width, height))

    # Updating the display
    pygame.display.update()

# Closes the window
pygame.quit()
