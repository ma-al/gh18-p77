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
    font = pygame.font.Font("../res/BebasNeue-Regular.ttf", 32)

    app = gui.App()
    timestepCtrl = TimestepControl()
    c = gui.Container(align=-1,valign=-1)
    c.add(timestepCtrl,0,0)

    app.init(c)

    camera_zoom = 1
    camera_pan = 0, 0

    # list of [(x,y), number]
    service_locations = load_service_locations()
    # print(service_locations)
    show_service_locations = False

    actmapGroup = pygame.sprite.GroupSingle()
    actmap = Map.Map(actmapGroup)
    pointIndicatorGroups = {}
    for dataset in ["aged_pops", "total_pops"]:
        pointIndicatorGroups[dataset] = {}
        # for year in range(2012, 2013):
        for year in range(2012, 2027):
            pointIndicatorGroups[dataset][year] = load_dataset("aged population", year, dataset)
    current_year = 2012
    current_dataset = "aged_pops"
    pointIndicatorGroup = pointIndicatorGroups[current_dataset][current_year]

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
            current_year = timestepCtrl.slider_year
            current_dataset = timestepCtrl.dataset
            pointIndicatorGroup = pointIndicatorGroups[current_dataset][current_year]
            show_service_locations = timestepCtrl.service


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
        camera = pygame.transform.smoothscale(camera, (int(width*camera_zoom), int(height*camera_zoom)))
        # draw to screen
        screen.fill(BLACK)
        if (show_service_locations):
            for text, (x,y) in service_locations:
                camera.blit(font.render(text, True, BLACK), (x,y))
        screen.blit(camera, camera_pan)
        screen.blit(font.render(str(current_dataset), True, BLACK), (width/2-100, 15))
        screen.blit(font.render(str(current_year), True, BLACK), (width/2-100, 40))

        # print(show_service_locations)

        app.paint()
        pygame.display.flip()

if __name__ == "__main__":
    main()