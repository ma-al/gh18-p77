import pygame
from colours import *

class PointIndicator(pygame.sprite.Sprite):

    # position: x,y from top left
    # value: float 0-1
    def __init__(self, position, value, group):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, group)

        self.image = pygame.image.load("../res/point_gradient.png")
        self.rect = self.image.get_rect()

        self.rect.center = position
        colour_value = tuple(map(lambda x: value*x, list(RED)))
        # colour_value = (value*RED[0]+value*BLUE[0],
        #                 value*RED[1]+value*BLUE[1],
        #                 value*RED[2]+value*BLUE[2])
        self.image.fill(colour_value, special_flags=pygame.BLEND_ADD)

class PostcodeIndicator(PostcodeIndicator):

    def __init__(self, postcode, value, group):
        PointIndicator.__init__(self, postcode_to_long_lat[postcode], value, group)




    
