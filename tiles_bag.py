import random

from tile import *


class TilesBag:
    def __init__(self):
        self.tiles = list()
        for _ in range(9):
            self.tiles.append(Tile("A"))
        for _ in range(8):
            self.tiles.append(Tile("I"))
        for _ in range(7):
            self.tiles.append(Tile("E"))
        for _ in range(6):
            self.tiles.append(Tile("O"))
        for _ in range(5):
            self.tiles.append(Tile("N"))
            self.tiles.append(Tile("Z"))
        for _ in range(4):
            self.tiles.append(Tile("R"))
            self.tiles.append(Tile("S"))
            self.tiles.append(Tile("W"))
            self.tiles.append(Tile("Y"))
        for _ in range(3):
            self.tiles.append(Tile("C"))
            self.tiles.append(Tile("D"))
            self.tiles.append(Tile("K"))
            self.tiles.append(Tile("L"))
            self.tiles.append(Tile("M"))
            self.tiles.append(Tile("P"))
            self.tiles.append(Tile("T"))
        for _ in range(2):
            self.tiles.append(Tile("B"))
            self.tiles.append(Tile("G"))
            self.tiles.append(Tile("H"))
            self.tiles.append(Tile("J"))
            self.tiles.append(Tile("Ł"))
            self.tiles.append(Tile("U"))
            self.tiles.append(Tile(" "))
        self.tiles.append(Tile("Ą"))
        self.tiles.append(Tile("Ę"))
        self.tiles.append(Tile("F"))
        self.tiles.append(Tile("Ó"))
        self.tiles.append(Tile("Ś"))
        self.tiles.append(Tile("Ż"))
        self.tiles.append(Tile("Ć"))
        self.tiles.append(Tile("Ń"))
        self.tiles.append(Tile("Ź"))

    def rand(self, nr):
        if nr > len(self.tiles):
            nr = len(self.tiles)
        random_elements = random.sample(self.tiles, nr)
        for element in random_elements:
            self.tiles.remove(element)
            element.x = random.randint(0, 14)
            element.y = random.randint(0, 14)
        return random_elements
