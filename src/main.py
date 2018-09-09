#!/usr/bin/python

import sys
import math
import random

import yaml
import pygame
from pgu import gui

from gui import TimestepControl
import Map
from postcode_lookups import *
from utilities import *
from colours import *

def main():
    # boilerplate and config
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font("../res/BebasNeue-Regular.ttf", 16)

    app = gui.App()
    timestepCtrl = TimestepControl()
    c = gui.Container(align=-1,valign=-1)
    c.add(timestepCtrl,0,0)

    app.init(c)

    camera_zoom = 1
    camera_pan = 0, 0

    actmapGroup = pygame.sprite.GroupSingle()
    actmap = Map.Map(actmapGroup)
    pointIndicatorGroups = {}
    for year in range(2012, 2028):
        pointIndicatorGroups[year] = load_dataset("aged population", year, "aged_pops")
    pointIndicatorGroup = pointIndicatorGroups[2012]

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
            app.event(event)

        if (timestepCtrl.new_dataset):
            timestepCtrl.new_dataset = False
            year = timestepCtrl.slider_year
            pointIndicatorGroup = pointIndicatorGroups[year]

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
        # for text, (x,y) in text_to_render:
        #     camera.blit(font.render(text, True, BLUE), (x,y))
        # camera = pygame.transform.smoothscale(camera, (int(width*camera_zoom), int(height*camera_zoom)))
        # draw to screen
        screen.fill(BLACK)
        screen.blit(camera, camera_pan)
        app.paint()
        pygame.display.flip()

if __name__ == "__main__":
    main()