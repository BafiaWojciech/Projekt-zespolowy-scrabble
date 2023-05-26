from grid import *
from tiles_box import *
from move_tile import *
from tiles_bag import *
from board import *

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([575, 625])

# Run until the user asks to quit
running = True
FPS = 60

grid = Grid(25, 25, 35)
tiles_box = TilesBox(25, 570, 35)
tile = Tile(*grid.get_position(3, 4), 35, "c")
tiles_box.add_tile(tile)

clock = pygame.time.Clock()

rectangle_dragging = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        try:
            rectangle_dragging = tile.drag_drop(event)
        except Exception:
            tile
    #screen.fill((255, 255, 255))
    screen.fill((15, 122, 72))

    if rectangle_dragging == False:
        tile.rect.x, tile.rect.y = grid.pull_up_position(tile.rect.x, tile.rect.y)
    grid.draw(screen)
    tiles_box.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
