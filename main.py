# Practicing using pygame
import pygame


# Initializes pygame
pygame.init()

# Creating a window
window = pygame.display.set_mode((500, 500))

# Adding a title to the window
pygame.display.set_caption("Practice game")

# Main game loop
run = True
while run:
    # Divide 1000 by the number below to get FPS estimate
    pygame.time.delay(100)

    # Event checker, reads through all recent events
    for event in pygame.event.get():
        # Checking if the game has been exited
        if event.type == pygame.quit():
            run = False

pygame.quit()
