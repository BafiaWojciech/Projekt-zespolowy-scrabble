from network import Network
from tiles_bag import *
from board import *
from button import *
from tile import Tile
import select
import string
import time

FPS = 60
window_width = 575
window_height = 650
rect_size = 35

running = True
dragging = False
start_index = (0, 0)
prev_pos = (0, 0)
motion = (0, 0)
new_index = None
pygame.font.init()
print("connecting to server")
n = Network()
print("connected")
board = Board(rect_size, n)

# TilesBag będzie po stronie serwera, tutaj użyte tylko do tego, aby mieć łatwy dostęp do płytek
tiles_bag = TilesBag()

for i in tiles_bag.rand(7):
    board.add_movable_tile(i)

pygame.init()
screen = pygame.display.set_mode([window_width, window_height])
clock = pygame.time.Clock()


print(len(string.ascii_uppercase))
elapsed = time.time()
SELECT_STEP = 1
sockets_list = [n.client]
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
        

        # test_str = "Hello"
        # serialized_object = pickle.dumps(test_str)
        # n.send(serialized_object)
        #print("recieve data")
        #sockets_list = [client_socket]

        #1
        # response_data = n.recv()
        # if response_data:
        #     print("Got response data")
        #     data = pickle.loads(response_data)
        #     print("adding to board")
        #     board.add_rigid_tile(data)


    
    board.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

    if time.time() - elapsed < SELECT_STEP:
        continue

    print('[INFO] Blocking on select')
    read_sockets, _, _ = select.select(sockets_list, [], [], 0)
    for notified_socket in read_sockets:
        print("notified_socket")
        response_data = n.recv()
        if response_data:
            print("Got response data")
            data = pickle.loads(response_data)
            print(data)
            print("adding to board")
            for t in data:
                board.add_rigid_tile(t)
    elapsed = time.time()            

pygame.quit()
