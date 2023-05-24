from grid import Grid
from tiles_box import TilesBox
import pygame
from tile import Tile

tile_color = (255, 225, 200)


class Board:
    def __init__(self, _rect_size):
        self.rect_size = _rect_size
        self.grid = Grid(25, 25, self.rect_size)
        self.tiles_box = TilesBox(25, 570, self.rect_size)
        self.rigid_tiles = []
        self.movable_tiles = []

        self.moved_tile = None
        self.motion = (0, 0)
        self.prev_pos = (0, 0)
        self.dragging = False

        self.font = pygame.font.Font('FreeSansBold.ttf', 26)

    def add_rigid_tile(self, tile):
        self.rigid_tiles.append(tile)

    def add_movable_tile(self, tile):
        if len(self.movable_tiles) < 7:
            for i in range(7):
                for t in self.movable_tiles:
                    if t.x == -1 and t.y == i:
                        break
                else:
                    tile.x = -1
                    tile.y = i
                    self.movable_tiles.append(tile)
                    break

    def move(self, _x, _y):
        if self.dragging:
            mouse_x, mouse_y = _x, _y
            self.motion = (self.motion[0] + mouse_x - self.prev_pos[0], self.motion[1] + mouse_y - self.prev_pos[1])
            self.prev_pos = (_x, _y)

    def drag_tile(self, _x, _y):
        self.prev_pos = _x, _y
        x, y = self.get_index(_x, _y)
        for t in self.movable_tiles:
            if t.x == x and t.y == y:
                self.moved_tile = t
                self.dragging = True
                return

    def stop_dragging(self, _x, _y):
        if not self.dragging:       #przy przesuwaniu elementu z "rigid_tiles" bez tego będzie wywalać błąd
            return
        final_index = self.get_index(_x, _y)
        if final_index[0] is not None:
            found = False
            for i in self.movable_tiles:
                if i.x == final_index[0] and i.y == final_index[1]:
                    found = True
            for i in self.rigid_tiles:
                if i.x == final_index[0] and i.y == final_index[1]:
                    found = True
            if not found:
                self.moved_tile.x, self.moved_tile.y = final_index
        self.moved_tile = None
        self.dragging = False
        self.motion = (0, 0)

    def get_position(self, _x, _y): #argumenty to pozycja okienka na planszy
        x = y = None
        if _x == -1 and 0 <= _y <= 6:
            x = 25 + self.rect_size * _y
            y = 570
        elif 0 <= _x <= 14 and 0 <= _y <= 14:
            x = 25 + self.rect_size * _x
            y = 25 + self.rect_size * _y
        return x+1, y+1

    def get_index(self, _x, _y): #argumenty to pozycja w pikselach względem rogu okna
        if 25 < _x < 550 and 25 < _y < 550:
            return (_x - 25) // self.rect_size, (_y - 25) // self.rect_size
        elif 25 < _x < 270 and 570 < _y < 605:
            return -1, (_x - 25) // self.rect_size
        else:
            return None, None

    def draw(self, screen):
        self.grid.draw(screen)
        self.tiles_box.draw(screen)

        for rt in self.rigid_tiles:
            rect = pygame.Rect(*self.get_position(rt.x, rt.y), self.rect_size - 2, self.rect_size - 2)
            pygame.draw.rect(screen, tile_color, rect, 0, 6)
            text = self.font.render(rt.letter, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        for mt in self.movable_tiles:
            offset = (0, 0)
            if mt == self.moved_tile:
                offset = self.motion
            rect = pygame.Rect(self.get_position(mt.x, mt.y)[0] + offset[0],
                               self.get_position(mt.x, mt.y)[1] + offset[1],
                               self.rect_size - 2, self.rect_size - 2)
            pygame.draw.rect(screen, tile_color, rect, 0, 6)
            text = self.font.render(mt.letter, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))
