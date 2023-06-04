# Practicing using pygame
import pygame
import numpy as np
import math

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
        # NOTE: this is also set when burning a tile, but it isn't displayed to the player
        self.team_id = team_id

        # Setting a tile id, which can be used to differentiate between tiles
        self.tile_id = x * x_bound + y

    def get_state(self):
        return self.state

    def get_tile_id(self):
        return self.tile_id

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
        # TODO Make the following conditional statement a function, as it is used in propagate_all
        if (next_x >= 0 & next_x < self.x_bound) & (next_y >= 0 & next_y < self.y_bound):
            self.tile_array[next_x, next_y].propagate(offset_x, offset_y, is_considering_movement)

    def propagate_all(self, is_considering_movement):
        # Calls nearby tiles to check if they should show that they can be used for movement
        if self.state == -2:
            for i in range(-1, 1):
                for j in range(-1, 1):
                    # Check if the locations are within bounds
                    if (self.x + i >= 0 & self.x + i < self.x_bound) & (self.y + j >= 0 & self.y + j < self.y_bound):
                        # If in bounds, then update
                        self.tile_array[self.x + i, self.y + j].propagate(i, j, is_considering_movement)


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

        # Setting up a default tile array considering node
        self.considering_id = -1

        # Creating a default Tile to the tile object, and creating an indicator to show that it shouldn't be used
        self.considering_tile = Tile
        self.valid_tile_considered = False

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

    def select_tile(self, x, y, team, is_moving):
        # Takes in the tile selection, and manipulates the board accordingly

        # DESIRED RETURN CHARACTERISTICS
        # It returns -1 if nothing changed,
        # 0 if the board changed but the action wasn't completed,
        # and 1 if the board changed, and the action was completed

        # CLARIFICATION OF WHAT RETURNING 1 MEANS:
        # For moving (is_moving True), 1 means the Amazon was moved.
        # For firing (is_moving False), 1 means a tile was blocked off

        selected_tile = self.tile_array[x, y]
        match selected_tile.get_state():
            case -2:
                if selected_tile.get_team_id() == team:
                    # If there is an amazon, and it is of the current team, then do the following:

                    if selected_tile.get_tile_id() == self.considering_id:
                        # If re-selecting the currently selected tile, then hide the movement options for it
                        self.considering_id = -1
                        self.selected_tile.propagate_all(False)

                        # Indicate that the stored tile is no longer being considered
                        self.valid_tile_considered = False
                    else:
                        # If selecting a new Amazon's tile, then do the following:

                        if self.valid_tile_considered:
                            # If there is a valid tile, then hide the movement options for that tile
                            self.considering_tile.propagate_all(False)

                        # Set the considering ID to the new id
                        # Show the movement options for the selected Amazon
                        self.considering_id = selected_tile.get_tile_id()
                        selected_tile.propagate_all(True)

                        # Indicate that this tile is being considered, and that it can be operated on
                        self.considering_tile = selected_tile
                        self.valid_tile_considered = True

                    # Indicate that the board has been changed, but the action has not been completed
                    return 0
            case 1:
                self.considering_id = -1
                if is_moving:
                    # If moving, then do the following:

                    # Remove all considering tile markers
                    # NOTE: If this is run before considering_tile is set, then it will cause problems
                    self.considering_tile.propagate_all(False)

                    # "Move" the Amazon from the considering tile to the new tile
                    selected_tile.set_info(-2, team)
                    self.considering_tile.set_info(0, 0)
                else:
                    # If firing, then do the following:

                    # Set the selected tile to be on fire
                    # Team ID is set just in case one wants to look at who burned what
                    selected_tile.set_info(-1, team)

                    # Indicate that the stored tile is no longer being considered
                    self.valid_tile_considered = False

                # Indicate that an action has been completed
                return 1

        # If none of the above conditions were met, then indicate that no changes have to be displayed.
        return -1


class GameManager:
    # Displays the state of the game
    # Sends requested inputs to TileManager, then displays the result
    def __init__(self, pixel_size=500, tile_side_count=10):
        # Creating a window
        self.window = pygame.display.set_mode((pixel_size, pixel_size))

        # Adding a title to the window
        pygame.display.set_caption("Game of the Amazons")

        # Creating tile_size, which can be used to segment the display and detect which tiles to update
        self.tile_size = pixel_size/tile_side_count
        self.tile_side_count = tile_side_count

        # Indicating that the movement step is being completed
        self.is_moving = True
        self.teams = 2
        # NOTE: turn increases every time a player finishes their two moves, so it's not really a turn counter
        # NOTE: turn is used to determine the current team playing by taking turn MOD teams
        self.turn = 0

        # Setting up the TileManager
        self.tile_manager = TileManager(tile_side_count)

    def find_current_team(self):
        # Take the modulo of turns to find the current team
        return self.turn % self.teams

    def click(self, input_x, input_y):
        # Translate a mouse click into a tile selection, then call select_tile
        x = math.floor(input_x / self.tile_size)
        y = math.floor(input_y / self.tile_size)
        self.select_tile(x, y)

    def select_tile(self, x, y):
        # Select a tile, get tile_manager to get an output, and dependent upon the response display the changes or call
        # action_finished if the action is done
        output = self.tile_manager.select_tile(x, y, self.find_current_team(), self.is_moving)
        if output == 1:
            self.action_finished()
        if output >= 0:
            self.display_all()

    def action_finished(self):
        # Describes what to do once an action has been completed
        # TODO: Add check to see if game is over, or the next player is out (if adding more than 2 player gameplay)

        # If the action wasn't movement, then increment the turn
        if ~self.is_moving:
            self.turn += 1

        # Switch to executing the other action type
        self.is_moving = ~self.is_moving

    def update_display(self):
        # Recalculate color for all rectangles
        # and update the window
        self.display_all()
        pygame.display.update()

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

game_manager = GameManager()

# Main game loop
run = True
game_manager.update_display()
while run:
    # Divide 1000 by the number below to get FPS estimate
    pygame.time.delay(100)

    # Event checker, reads through all recent events
    for event in pygame.event.get():
        # Checking if the game has been exited
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game_manager.click(mouse_x, mouse_y)



# Closes the window
pygame.quit()
