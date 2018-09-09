#!/usr/bin/python

import sys
import pygame
import Map
import PointIndicator
import random
from colours import *
from postcode_to_long_lat import *

# at this point long-lat = -35.10, 148.55
TOP_LEFT_MAP_OFFSET = 173, 384
# at this point long-lat = -35.25, 149.15
BOTTOM_RIGHT_MAP_OFFSET = 1713, 1799

# some constants used in equirectangular_projection
# a latitude in the centre of our map
CENTRAL_LAT = (148.55 + 149.15)/2

# convert long lat to x,y
def equirectangular_projection(long, lat)
    x = math.cos()


def main():

    # boilerplate and config
    pygame.init()
    size = width, height = 1000, 1000 
    screen = pygame.display.set_mode(size)

    actmapGroup = pygame.sprite.GroupSingle()
    actmap = Map.Map(actmapGroup)
    pointIndicatorGroup = pygame.sprite.Group()

    pointIndicators = []
    for name,long,lat in postcode_to_long_lat.values():



        pi = PointIndicator.PointIndicator((random.random()*height, random.random()*height), random.random(), pointIndicatorGroup)
        pointIndicators.append(pi)

    filters = []

    # main loop
    while 1:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.QUIT: 
                sys.exit()
        
        # rendering        
        screen.fill(BLACK)
        actmapGroup.draw(screen)
        pointIndicatorGroup.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()