import pygame
from tile import *

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

black = (0, 0, 0)
light_blue = (25, 183, 194)
dark_blue = (15, 89, 250)
pink = (255, 120, 228)
red = (250, 50, 77)


class Grid:
    def __init__(self, _x, _y, rect_size):
        self.x = _x
        self.y = _y
        self.rect_size = rect_size

    def draw(self, screen):
        screen.fill((15, 122, 72))
        for i in range(0, 15):
            for j in range(0, 15):
                _x = self.x + i * self.rect_size
                _y = self.y + j * self.rect_size
                rect = pygame.Rect(_x, _y, self.rect_size, self.rect_size)

                bonus = bonsu_field.get((i, j))
                if bonus == "W3":
                    pygame.draw.rect(screen, red, rect)
                elif bonus == "W2":
                    pygame.draw.rect(screen, pink, rect)
                elif bonus == "L3":
                    pygame.draw.rect(screen, dark_blue, rect)
                elif bonus == "L2":
                    pygame.draw.rect(screen, light_blue, rect)
                pygame.draw.rect(screen, black, rect, 1)

    def get_position(self, i, j):
        return self.x + i * self.rect_size, self.y + j * self.rect_size
