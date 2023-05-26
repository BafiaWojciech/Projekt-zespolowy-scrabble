from tiles_bag import *
from board import *
from button import *
import string

FPS = 60
window_width = 575
window_height = 625
rect_size = 35

running = True
dragging = False
start_index = (0, 0)
prev_pos = (0, 0)
motion = (0, 0)
new_index = None
pygame.font.init()
board = Board(rect_size)

# TilesBag będzie po stronie serwera, tutaj użyte tylko do tego, aby mieć łatwy dostęp do płytek
tiles_bag = TilesBag()

for i in tiles_bag.rand(7):
    board.add_movable_tile(i)

pygame.init()
screen = pygame.display.set_mode([window_width, window_height])
clock = pygame.time.Clock()

print(len(string.ascii_uppercase))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.mouse_button_down(*event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            board.mouse_button_up(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            board.move(*event.pos)

    board.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
