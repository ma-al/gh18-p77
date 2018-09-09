import pygame

class Map(pygame.sprite.Sprite):

    def __init__(self, group):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, group)

        self.image = pygame.image.load("../res/map.png")
        self.rect = self.image.get_rect()

    def update():
        pass