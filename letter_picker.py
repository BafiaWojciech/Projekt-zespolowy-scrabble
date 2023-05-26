import pygame


class LetterPicker:
    def __init__(self):
        self.x = 25
        self.y = 25
        self.margin = 10
        self.padding = 5
        self.letter_size = 28
        self.width = 8 * self.letter_size + 7 * self.padding + self.margin * 2
        self.height = 4 * self.letter_size + 3 * self.padding + self.margin * 2

        self.font = pygame.font.Font('FreeSansBold.ttf', 18)

        self.letters = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń',
                        'o', 'ó', 'p', 'r', 's', 'ś', 't', 'u', 'w', 'y', 'z', 'ź', 'ż']

    def check_click(self, _x, _y):
        if _x < self.x + self.margin or _y < self.y + self.margin or self.x + self.width - self.margin < _x or self.y + self.height - self.margin < _y:
            return "0"

        index_x = (_x - self.x - self.margin) // (self.letter_size + self.padding)
        index_y = (_y - self.y - self.margin) // (self.letter_size + self.padding)
        l = self.letters[index_x + index_y * 8].upper()
        print(l)
        return l

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 225, 200), rect, 0)

        for i in range(len(self.letters)):
            rect = pygame.Rect(self.x + self.margin + i % 8 * (self.letter_size + self.padding),
                               self.y + self.margin + i // 8 * (self.letter_size + self.padding), self.letter_size,
                               self.letter_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 0, 3)
            text = self.font.render(self.letters[i].upper(), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))
