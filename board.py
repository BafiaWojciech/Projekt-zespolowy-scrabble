from grid import Grid
from tiles_box import TilesBox
from button import Button
from letter_picker import LetterPicker
import pygame

from tiles_bag import *

tile_color = (247, 247, 215)

points_for_letter = {
    'A': 1,
    'Ą': 5,
    'B': 3,
    'C': 2,
    'Ć': 6,
    'D': 2,
    'E': 1,
    'Ę': 5,
    'F': 5,
    'G': 3,
    'H': 3,
    'I': 1,
    'J': 3,
    'K': 2,
    'L': 2,
    'Ł': 3,
    'M': 2,
    'N': 1,
    'Ń': 7,
    'O': 1,
    'Ó': 5,
    'P': 2,
    'R': 1,
    'S': 1,
    'Ś': 5,
    'T': 2,
    'U': 3,
    'W': 1,
    'Y': 2,
    'Z': 1,
    'Ź': 9,
    'Ż': 5,
    ' ': 0
}

bonsu_field = {
    (0, 0): "W3", (0, 7): "W3", (0, 14): "W3",
    (7, 0): "W3", (7, 14): "W3", (14, 0): "W3",
    (14, 7): "W3", (14, 14): "W3", (1, 1): "W2",
    (2, 2): "W2", (3, 3): "W2", (4, 4): "W2",
    (10, 4): "W2", (11, 3): "W2", (12, 2): "W2",
    (13, 1): "W2", (4, 10): "W2", (3, 11): "W2",
    (2, 12): "W2", (1, 13): "W2", (10, 10): "W2",
    (11, 11): "W2", (12, 12): "W2", (13, 13): "W2",
    (7, 7): "W2", (1, 5): "L3", (5, 1): "L3",
    (1, 9): "L3", (9, 1): "L3", (5, 5): "L3",
    (9, 5): "L3", (5, 9): "L3", (13, 5): "L3",
    (9, 9): "L3", (5, 13): "L3", (13, 9): "L3",
    (9, 13): "L3", (3, 0): "L2", (0, 3): "L2",
    (6, 2): "L2", (2, 6): "L2", (7, 3): "L2",
    (3, 7): "L2", (8, 2): "L2", (2, 8): "L2",
    (11, 0): "L2", (0, 11): "L2", (6, 6): "L2",
    (3, 14): "L2", (14, 3): "L2", (8, 6): "L2",
    (6, 8): "L2", (8, 8): "L2", (12, 6): "L2",
    (6, 12): "L2", (11, 7): "L2", (7, 11): "L2",
    (12, 8): "L2", (8, 12): "L2", (14, 11): "L2",
    (11, 14): "L2"
}

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
            text = self.font.render(rt.letter[-1] + str(points_for_letter[rt.letter[0]]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        for mt in self.movable_tiles:
            offset = (0, 0)
            if mt == self.moved_tile:
                offset = self.motion
            rect = pygame.Rect(self.get_position(mt.x, mt.y)[0] + offset[0],
                               self.get_position(mt.x, mt.y)[1] + offset[1],
                               self.rect_size - 2, self.rect_size - 2)
            pygame.draw.rect(screen, (255, 255, 255), rect, 0, 6)
            text = self.font.render(mt.letter[-1] + str(points_for_letter[mt.letter[0]]), True, (0, 0, 0))
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

            wrong = True
            for t in tmp:
                if board[t.x - 1][t.y] is not None or \
                        board[t.x + 1][t.y] is not None or \
                        board[t.x][t.y - 1] is not None or \
                        board[t.x][t.y + 1] is not None:
                    wrong = False
                    break

            if wrong:
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

        points = 0
        perpendicular_words_points = 0
        total_word_bonus = 1

        #if len(tmp) != 1:
        min_x = min(tmp, key=lambda tmp: tmp.x)
        min_y = min(tmp, key=lambda tmp: tmp.y)
        max_x = max(tmp, key=lambda tmp: tmp.x)
        max_y = max(tmp, key=lambda tmp: tmp.y)

        if min_x == max_x:  # pionowo
            print("pionowo")
            top = min_y
            bottom = max_y
            while board[top.x][top.y - 1] is not None:
                top = board[top.x][top.y - 1]
            while bottom.y + 1 < len(board[bottom.x]) and board[bottom.x][bottom.y + 1] is not None:
                bottom = board[bottom.x][bottom.y + 1]
            for i in range(top.y, bottom.y + 1):
                if board[top.x][i] is None:
                    self.points_info = "nie ma ciągłości w pionie a"
                    return False
                else:           # liczenie punktów
                    l = board[top.x][i]
                    points += points_for_letter[l.letter[0]]
                    for t in tmp:
                        if (t.x, t.y) == (l.x, l.y):    #jeżeli litera jest z movabletiles na planszy
                            left = l
                            right = l
                            while board[left.x - 1][left.y] is not None:
                                left = board[left.x - 1][left.y]
                            while right.x + 1 < len(board) and board[right.x + 1][right.y] is not None:
                                right = board[right.x + 1][right.y]
                            tmp_points = 0
                            for i in range(left.x, right.x + 1):
                                a = board[i][left.y]
                                tmp_points += points_for_letter[a.letter[0]]
                            tmp_points = tmp_points - points_for_letter[l.letter[0]]
                            bonus = bonsu_field.get((l.x,l.y), " 1")
                            if bonus[0] == 'W':
                                tmp_points *= int(bonus[1])
                                total_word_bonus *= int(bonus[1])
                            if bonus[0] == 'L':
                                points += (points_for_letter[l.letter[0]] * ((int(bonus[1])) - 1))
                            perpendicular_words_points += tmp_points
                            break

        elif min_y == max_y:  # poziomo
            print("poziomo")
            left = min_x
            right = max_x
            while board[left.x - 1][left.y] is not None:
                left = board[left.x - 1][left.y]
            while right.x + 1 < len(board) and board[right.x + 1][right.y] is not None:
                right = board[right.x + 1][right.y]
            for i in range(left.x, right.x + 1):
                if board[i][left.y] is None:
                    self.points_info = "nie ma ciągłości w poziomie b"
                    return False
                else:           # liczenie punktów
                    l = board[i][left.y]
                    points += points_for_letter[l.letter[0]]
                    for t in tmp:
                        if (t.x, t.y) == (l.x, l.y):    #jeżeli litera jest nowa
                            top = l
                            bottom = l
                            while board[top.x][top.y - 1] is not None:
                                top = board[top.x][top.y - 1]
                            while bottom.y + 1 < len(board[bottom.x]) and board[bottom.x][bottom.y + 1] is not None:
                                bottom = board[bottom.x][bottom.y + 1]
                            tmp_points = 0
                            for i in range(top.y, bottom.y + 1):
                                a = board[i][left.y]
                                a = board[top.x][i]
                                tmp_points += points_for_letter[a.letter[0]]
                            tmp_points = tmp_points - points_for_letter[l.letter[0]]
                            bonus = bonsu_field.get((l.x, l.y), " 1")
                            if bonus[0] == 'W':
                                tmp_points *= int(bonus[1])
                                total_word_bonus *= int(bonus[1])
                            if bonus[0] == 'L':
                                points += (points_for_letter[l.letter[0]] * ((int(bonus[1])) - 1))
                            perpendicular_words_points += tmp_points
                            break

        else:
            self.points_info = "nie w jednej linii"
            return False

        points *= total_word_bonus
        points += perpendicular_words_points
        if len(tmp) == 7:
            points += 50
        self.points_info = "punkty: " + str(points)
        print()

        return True
