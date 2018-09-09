import pygame
from colours import *
from utilities import *
from postcode_lookups import *

class PointIndicator(pygame.sprite.Sprite):

    # position: x,y from top left
    # value: float 0-1
    def __init__(self, position, value, group):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, group)

        self.image = pygame.image.load("../res/point.png")
        self.rect = self.image.get_rect()

        self.rect.center = position
        colour_value = (255*value, 0, 255*(1-value))
        self.image.fill(colour_value, special_flags=pygame.BLEND_MULT)
        self.image = pygame.transform.scale(self.image, (round(self.rect.width*value), round(self.rect.height*value)))
        
        self.rect = self.image.get_rect()
        self.rect.center = position

class PostcodeIndicator(PointIndicator):

    def __init__(self, postcode, value, group):
        _, long, lat = postcode_to_lat_long[postcode]
        x, y = long_lat_to_x_y(long, lat)
        PointIndicator.__init__(self, (long, lat) , value, group)

