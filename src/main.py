#!/usr/bin/python

import sys
import math
import random

import pygame
import numpy

import Map
from PointIndicator import PointIndicator, PostcodeIndicator 
from postcode_to_lat_long import *
from utilities import *
from colours import *

def main():
    # boilerplate and config
    pygame.init()
    pygame.font.init()
    size = width, height = 750, 1499 
    map_width, map_height = 750, 1499
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font("../res/BebasNeue-Regular.ttf", 16)

    camera_zoom = 1
    camera_pan = 0, 0

    actmapGroup = pygame.sprite.GroupSingle()
    actmap = Map.Map(actmapGroup)
    pointIndicatorGroup = pygame.sprite.Group()

    text_to_render = [] # list of (string, (x,y))
    xs = []
    ys = []
    names = []
    for _,name,lat,long in postcode_lat_long_list:
        x, y = lat_long_to_x_y(lat, long)
        xs.append(x)
        ys.append(y)
        names.append(name)

    max_x = max(xs)
    min_x = min(xs)
    max_y = max(ys)
    min_y = min(ys)

    print(names[xs.index(min_x)])
    print(names[xs.index(max_x)])
    print(names[ys.index(min_y)])
    print(names[ys.index(max_y)])

    # normalise
    for i in range(len(xs)):
        x = (xs[i] - max_x) / (max_x - min_x)
        y = -(ys[i] - max_y) / (max_y - min_y)
        # print(x, y)
        x *= map_width
        y *= map_height
        x += width
        pi = PointIndicator((x,y), 1, pointIndicatorGroup)
        text_to_render.append((names[i], (x, y)))

    # main loop
    done = False
    while not done:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.QUIT: 
                done = True
        
        # camera movement
        if pygame.key.get_pressed()[pygame.K_w]:
            camera_pan = camera_pan[0], camera_pan[1] + 10*camera_zoom
        if pygame.key.get_pressed()[pygame.K_s]:
            camera_pan = camera_pan[0], camera_pan[1] - 10*camera_zoom
        if pygame.key.get_pressed()[pygame.K_a]:
            camera_pan = camera_pan[0] + 10*camera_zoom, camera_pan[1]
        if pygame.key.get_pressed()[pygame.K_d]:
            camera_pan = camera_pan[0] - 10*camera_zoom, camera_pan[1]
        if pygame.key.get_pressed()[pygame.K_r]:
            camera_zoom += 0.1
        if pygame.key.get_pressed()[pygame.K_f]:
            # prevent scaling of 0
            if (camera_zoom > 0.1):
                camera_zoom -= 0.1

        # rendering
        # draw to camera surface first so we can transform it
        camera = pygame.Surface((width, height))
        actmapGroup.draw(camera)
        pointIndicatorGroup.draw(camera)
        for text, (x,y) in text_to_render:
            camera.blit(font.render(text, True, BLUE), (x,y))
        # camera = pygame.transform.smoothscale(camera, (int(width*camera_zoom), int(height*camera_zoom)))
        # draw to screen
        screen.fill(BLACK)
        screen.blit(camera, camera_pan)
        pygame.display.flip()

if __name__ == "__main__":
    main()