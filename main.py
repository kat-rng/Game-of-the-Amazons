# Practicing using pygame
import pygame
import numpy as np


class Tile:
    # The core game logic element
    # Defines what each tile should be displayed as through the state variable
    # Controls the core game logic through its various functions
    # Frequently uses "recursive" calls via the tile_array

    def __init__(self, tile_array, x, y, x_bound, y_bound, state, team_id=-1):
        # tile_array is an array of Tile objects. It should be provided by the TileManager
        self.tile_array = tile_array

        # Setting x and y location along with boundaries from initialization call parameters
        self.x = x
        self.y = y
        self.x_bound = x_bound
        self.y_bound = y_bound

        # Setting state variable, which describes how the tile should be displayed
        # -2 means an amazon is on the tile. -1 means the tile is inaccessible.
        # 0 means the tile is empty, and 1 means it is empty, and it is being considered for movement
        self.state = state

        # Setting a team id, which can be used to identify which color to display amazons as
        self.team_id = team_id

    def get_state(self):
        return self.state

    def get_team_id(self):
        return self.team_id

    def set_info(self, state, team_id=-1):
        self.state = state
        self.team_id = team_id

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

        # Checking if the next location crosses a boundary
        # If not, then continue the chain of calls
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

        # Setting the locations of the Amazons
        self.default_locations()

    def default_locations(self):
        # Setting the locations to the standard amazons board layout
        self.tile_array[3, 0].set_info(-2, 0)
        self.tile_array[6, 0].set_info(-2, 0)
        self.tile_array[0, 3].set_info(-2, 0)
        self.tile_array[9, 3].set_info(-2, 0)

        self.tile_array[3, 9].set_info(-2, 1)
        self.tile_array[6, 9].set_info(-2, 1)
        self.tile_array[0, 6].set_info(-2, 1)
        self.tile_array[9, 6].set_info(-2, 1)

    def get_tile(self, x, y):
        return self.tile_array[x, y]


class DisplayManager:
    # Displays the state of the game
    # Sends requested inputs to TileManager, then displays the result
    def __init__(self, pixel_size=500, tile_side_count=10):
        # Creating a window
        self.window = pygame.display.set_mode((pixel_size, pixel_size))

        # Creating tile_size, which can be used to segment the display and detect which tiles to update
        self.tile_size = pixel_size/tile_side_count
        self.tile_manager = TileManager(tile_side_count)
        self.tile_side_count = tile_side_count

        # Adding a title to the window
        pygame.display.set_caption("Game of the Amazons")

    def display_tile(self, x, y):
        # Getting the pixel location to draw the tile at
        x_location = x * self.tile_size
        y_location = y * self.tile_size

        # Drawing the tile according to the color from grab_tile_color
        pygame.draw.rect(self.window, self.grab_tile_color(x, y),
                         (x_location, y_location, self.tile_size, self.tile_size))

    def grab_tile_color(self, x, y):
        tile = self.tile_manager.get_tile(x, y)

        # Use the tile state to determine the color that should be displayed for that tile
        match tile.get_state():
            case 0:
                # Empty
                return pygame.Color(128, 128, 128)
            case -1:
                # On fire/ inaccessible
                return pygame.Color(255, 0, 0)
            case 1:
                # Empty, but being considered for movement
                return pygame.Color(255, 255, 0)
            case -2:
                # Amazon
                team = tile.get_team_id()
                if team == 0:
                    return pygame.Color(0, 255, 0)
                elif team == 1:
                    return pygame.Color(0, 0, 255)
                else:
                    print("Invalid team ID 135")
        print("Invalid tile state")
        print("x location ", x, " y location ", y)

    def display_all(self):
        for x in range(self.tile_side_count):
            for y in range(self.tile_side_count):
                self.display_tile(x, y)

# START OF GAME CODE

# Initializes pygame
pygame.init()

display = DisplayManager()

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


    # Display all tile locations
    display.display_all()

    # Updating the display
    pygame.display.update()

# Closes the window
pygame.quit()
