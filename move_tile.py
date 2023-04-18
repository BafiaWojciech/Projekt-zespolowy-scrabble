import pygame

tile_color = (255, 225, 150)


class display_tile:
    def __init__(self, _x, _y, _rect_size, _letter):
        self.letter = _letter
        self.rect = pygame.Rect(_x, _y, _rect_size, _rect_size)
        self.rectangle_dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, tile_color, self.rect, 0, 6)

    def drag_drop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.rectangle_dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.rectangle_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.rectangle_dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

        return self.rectangle_dragging
