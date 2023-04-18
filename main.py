from tiles_bag import *
from board import *

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

board = Board(rect_size)

    #TilesBag będzie po stronie serwera, tutaj użyte tylko do tego, aby mieć łatwy dostęp do płytek
tiles_bag = TilesBag()
    #TilesBag losuje pozycje płytek, dlatego tutaj obiektom 'movable_tiles' ręcznie ustawiam pozycje
movable_tiles = tiles_bag.rand(7)
print("movable_tiles")
for i in range(7):
    movable_tiles[i].x = -1
    movable_tiles[i].y = i
    print(movable_tiles[i].letter, movable_tiles[i].x, movable_tiles[i].y)

print("rigid_tiles")
rigid_tiles = tiles_bag.rand(10)
for i in rigid_tiles:
    print(i.letter, i.x, i.y)

pygame.init()
screen = pygame.display.set_mode([window_width, window_height])
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            index_x, index_y = board.get_index(*event.pos)
            if index_x is not None:
                start_index = index_x, index_y
                dragging = True
                prev_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            start_position = board.get_position(*start_index)
            final_position = (start_position[0] + motion[0] + rect_size / 2,
                              start_position[1] + motion[1] + rect_size / 2)
            final_index = board.get_index(*final_position)
            # TODO w tym miejscu powinno się sprawdzać, czy miejsce w którym chcemy położyć płytkę nie jest już zajęte
            if final_index[0] is not None:
                new_index = final_index
            motion = prev_pos = [0, 0]
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                motion = (motion[0] + mouse_x - prev_pos[0], motion[1] + mouse_y - prev_pos[1])
                prev_pos = event.pos

    #board
    board.draw(screen)
    for rt in rigid_tiles:
        rect = pygame.Rect(*board.get_position(rt.x, rt.y), rect_size - 2, rect_size - 2)
        pygame.draw.rect(screen, (255, 225, 150), rect, 0, 6)
    for mt in movable_tiles:
        offset = (0, 0)
        if (mt.x, mt.y) == start_index:
            if dragging:
                offset = motion
            elif new_index is not None:
                mt.x, mt.y = new_index
                new_index = None
                start_index = None
        rect = pygame.Rect(board.get_position(mt.x, mt.y)[0] + offset[0],
                           board.get_position(mt.x, mt.y)[1] + offset[1],
                           rect_size - 2, rect_size - 2)
        pygame.draw.rect(screen, (255, 255, 250), rect, 0, 6)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
