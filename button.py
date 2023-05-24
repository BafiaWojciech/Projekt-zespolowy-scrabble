import pygame


class Button:
    def __init__(self, name, _x, _y, width, height):
        self.name = name
        self.x = _x
        self.y = _y
        self.width = width
        self.height = height
        self.font = pygame.font.Font('FreeSansBold.ttf', 20)

    def check_click(self, _x, _y):
        return True if self.x < _x < self.x + self.width and self.y < _y < self.y + self.height else False

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 225, 200), rect, 0)

        text = self.font.render(self.name, True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))
