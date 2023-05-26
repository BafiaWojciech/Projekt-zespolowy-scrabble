import pygame


class TilesBox:

    def __init__(self, _x, _y, _rect_size):
        self.tiles = []
        self.x = _x
        self.y = _y
        self.rect_size = _rect_size

    def draw(self, screen):
        color = (0, 0, 0)
        for i in range(7):
            _x = self.x + i * self.rect_size
            rect = pygame.Rect(_x, self.y, self.rect_size, self.rect_size)
            pygame.draw.rect(screen, color, rect, 1)

