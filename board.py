from grid import Grid
from tiles_box import TilesBox
from button import Button
from letter_picker import LetterPicker
import pygame

from tiles_bag import *

tile_color = (247, 247, 215)


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
        self.info_font = pygame.font.Font('FreeSansBold.ttf', 18)
        self.swap_button = Button("wymień", 280, 570, 80, 35)
        self.send_button = Button("wyślij", 375, 570, 80, 35)
        self.pass_button = Button("pasuj", 470, 570, 80, 35)

        self.points_info = ""
        self.pick_letter = False
        self.letter_picker = LetterPicker()

    def draw(self, screen):
        self.grid.draw(screen)
        self.tiles_box.draw(screen)
        self.send_button.draw(screen)
        self.swap_button.draw(screen)
        self.pass_button.draw(screen)

        for rt in self.rigid_tiles:
            rect = pygame.Rect(*self.get_position(rt.x, rt.y), self.rect_size - 2, self.rect_size - 2)
            pygame.draw.rect(screen, tile_color, rect, 0, 6)
            text = self.font.render(rt.letter[-1], True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        for mt in self.movable_tiles:
            offset = (0, 0)
            if mt == self.moved_tile:
                offset = self.motion
            rect = pygame.Rect(self.get_position(mt.x, mt.y)[0] + offset[0],
                               self.get_position(mt.x, mt.y)[1] + offset[1],
                               self.rect_size - 2, self.rect_size - 2)
            pygame.draw.rect(screen, (255, 255, 255), rect, 0, 6)
            text = self.font.render(mt.letter[-1], True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        points = self.info_font.render(self.points_info, True, (0, 0, 0))
        screen.blit(points, points.get_rect(center=pygame.Rect(0, 0, 575, 28).center))

        if self.pick_letter:
            self.letter_picker.draw(screen)

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

    def mouse_button_down(self, _x, _y):

        if self.pick_letter:
            letter = self.letter_picker.check_click(_x, _y)
            if letter.isalpha():
                self.pick_letter = False
                self.moved_tile.letter = " " + letter
            elif self.moved_tile.letter[-1].isupper():
                self.pick_letter = False
        else:
            self.drag_tile(_x, _y)
            if self.send_button.check_click(_x, _y):
                if self.validate_board_placement():
                    print("wyślij")

                    # to dokładanie liter powinno odbywać się po stronie serwera
                    tmp = [t for t in self.movable_tiles if t.x != -1]
                    for t in tmp:
                        print(t.letter, t.x, t.y)
                        self.rigid_tiles.append(t)
                        self.movable_tiles.remove(t)

                    # w tym miejscu z serwera powinniśmy dostać wylosowane literki
                    tiles_bag = TilesBag()
                    for i in tiles_bag.rand(len(tmp)):
                        self.add_movable_tile(i)

            if self.swap_button.check_click(_x, _y):
                print("wymień")

            if self.pass_button.check_click(_x, _y):
                print("pasuj")
                for i, t in enumerate(self.movable_tiles):
                    t.letter = t.letter[0]
                    t.x = -1
                    t.y = i

    def mouse_button_up(self, _x, _y):
        self.stop_dragging(_x, _y)
        self.validate_board_placement()

    def drag_tile(self, _x, _y):
        self.pick_letter = False
        self.prev_pos = _x, _y
        x, y = self.get_index(_x, _y)
        for t in self.movable_tiles:
            if t.x == x and t.y == y:
                self.moved_tile = t
                self.dragging = True
                break

    def move(self, _x, _y):
        if self.dragging:
            mouse_x, mouse_y = _x, _y
            self.motion = (self.motion[0] + mouse_x - self.prev_pos[0], self.motion[1] + mouse_y - self.prev_pos[1])
            self.prev_pos = (_x, _y)

    def stop_dragging(self, _x, _y):
        if not self.dragging:
            return
        final_index = self.get_index(_x, _y)

        if final_index[0] is not None:
            if self.moved_tile.letter.startswith(" "):
                if final_index[0] == -1:
                    self.moved_tile.letter = " "
                else:
                    self.pick_letter = True
                    self.dragging = False
            found = False
            for i in self.movable_tiles:
                if i.x == final_index[0] and i.y == final_index[1]:
                    found = True
            for i in self.rigid_tiles:
                if i.x == final_index[0] and i.y == final_index[1]:
                    found = True
            if not found:
                self.moved_tile.x, self.moved_tile.y = final_index
        self.dragging = False
        self.motion = (0, 0)

    def get_position(self, _x, _y):  # argumenty to pozycja okienka na planszy
        x = y = None
        if _x == -1 and 0 <= _y <= 6:
            x = 25 + self.rect_size * _y
            y = 570
        elif 0 <= _x <= 14 and 0 <= _y <= 14:
            x = 25 + self.rect_size * _x
            y = 25 + self.rect_size * _y
        return x + 1, y + 1

    def get_index(self, _x, _y):  # argumenty to pozycja w pikselach względem rogu okna
        if 25 < _x < 550 and 25 < _y < 550:
            return (_x - 25) // self.rect_size, (_y - 25) // self.rect_size
        elif 25 < _x < 270 and 570 < _y < 605:
            return -1, (_x - 25) // self.rect_size
        else:
            return None, None

    def validate_board_placement(self):
        self.points_info = ""
        tmp = [t for t in self.movable_tiles if t.x != -1]
        if len(tmp) == 0:
            return False

        board = [[None] * 16 for _ in range(16)]

        if len(self.rigid_tiles) != 0:
            for t in self.rigid_tiles:
                board[t.x][t.y] = t

            for t in self.movable_tiles:
                if board[t.x - 1][t.y] is not None or \
                        board[t.x + 1][t.y] is not None or \
                        board[t.x][t.y - 1] is not None or \
                        board[t.x][t.y + 1] is not None:
                    break
            else:
                self.points_info = "nieprawidłowy ruch - nie ma styku z płytkami na planszy"
                return False

            for t in self.movable_tiles:
                board[t.x][t.y] = t

        else:
            for t in self.movable_tiles:
                board[t.x][t.y] = t
            if board[7][7] is None:
                self.points_info = "pierwszy ruch musi przechodzic przez środek planszy"
                return False

        if len(tmp) != 1:
            min_x = min(tmp, key=lambda tmp: tmp.x)
            min_y = min(tmp, key=lambda tmp: tmp.y)
            max_x = max(tmp, key=lambda tmp: tmp.x)
            max_y = max(tmp, key=lambda tmp: tmp.y)
            if min_x != max_x and min_y != max_y:
                self.points_info = "nie w jednej linii"
                return False

            if min_x == max_x:  # pionowo
                top = min_y
                bottom = max_y
                i = 1
                while board[top.x][top.y - i] is not None:
                    top = board[top.x][top.y - i]
                    i = i + 1
                i = 1
                while board[bottom.x][bottom.y + i] is not None:
                    bottom = board[bottom.x][bottom.y + i]
                    i = i + 1
                for i in range(top.y, bottom.y + 1):
                    if board[top.x][i] is None:
                        self.points_info = "nie ma ciągłości w pionie"
                        return False

            if min_y == max_y:  # poziomo
                left = min_x
                right = max_x
                i = 1
                while board[left.x - i][left.y] is not None:
                    left = board[left.x - i][left.y]
                    i = i + 1
                i = 1
                while board[right.x + i][right.y] is not None:
                    right = board[right.x + i][right.y]
                    i = i + 1
                for i in range(left.x, right.x + 1):
                    if board[i][left.y] is None:
                        self.points_info = "nie ma ciągłości w poziomie"
                        return False

        points = 0
        # tu liczenie punktów
        self.points_info = "punkty: " + str(points)

        return True
