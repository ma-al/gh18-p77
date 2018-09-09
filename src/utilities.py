import sys
import math
import utm

import yaml
import pygame
from PointIndicator import PointIndicator, PostcodeIndicator 
from postcode_lookups import *
from utilities import *
from colours import *

def lat_long_to_x_y(lat, long):
    x,y,_,_ = utm.from_latlon(lat, long)
    return x, y

size = width, height = 750, 1499 
map_width, map_height = 750, 1499

# normalise a generic array of numbers 
def normalise(xs):
    norm_xs = []

    max_x = max(xs)
    min_x = min(xs)

    if max_x == min_x: return xs

    # normalise
    for i in range(len(xs)):
        x = -(xs[i] - max_x) / (max_x - min_x)
        norm_xs.append(x)
    return norm_xs    

# normalise utm coords with respect to our map
def normalise_utm_coords(xs, ys):
    norm_xs = []
    norm_ys = []

    max_x = max(xs)
    min_x = min(xs)
    max_y = max(ys)
    min_y = min(ys)

    if max_x == min_x or max_y == min_y:
        return xs, ys


    # normalise
    for i in range(len(xs)):
        x = (xs[i] - max_x) / (max_x - min_x)
        y = -(ys[i] - max_y) / (max_y - min_y)
        # print(x, y)
        x *= map_width
        y *= map_height
        x += width

        norm_xs.append(x)
        norm_ys.append(y)
    return norm_xs, norm_ys

# return a list of (text, (x,y)) and a pointIndicatorGroup to render
def load_dataset(dataset, queried_year, queried_value):
    pointIndicatorGroup = pygame.sprite.Group()

    if dataset == "aged population":
        stream = open("../data/output/data.yml")
        xs = []
        ys = []
        indices = []
        total_pops = []
        aged_pops = []
        proportional_pops = []
        for data in yaml.load_all(stream):
            for k in data.keys():
                # import pdb; pdb.set_trace()
                sa2_name = data[k]["sa2_name"]

                index = 0
                elder_population = 0
                total_population = 0
                proportional_pop = 0
                for year in data[k]["by_year"]:
                    if (year['year'] != queried_year): 
                        continue
                    index = year["index"]
                    elder_population = year["elder_population"]
                    total_population = year["total_population"]
                    if not total_population == 0:
                        proportional_pop = year["elder_population"] / year["total_population"]

                # skip if we can't find a lat long
                try:
                    lat,long = name_to_lat_long[sa2_name.rstrip(" (ACT)").upper()]
                except KeyError:
                    # print ("can't find long lat for '" + sa2_name.rstrip(" (ACT)").upper() +"'")
                    continue
                x,y = lat_long_to_x_y(lat, long)
                xs.append(x)
                ys.append(y)

                total_pops.append(total_population)
                aged_pops.append(elder_population)
                proportional_pops.append(proportional_pop)
                indices.append(index)
        # print(len(xs))
        xs, ys = normalise_utm_coords(xs, ys)
        total_pops = normalise(total_pops)
        aged_pops = normalise(aged_pops)
        proportional_pops = normalise(proportional_pops)
        indices = normalise(indices)

        values = {"total_pops":total_pops, "aged_pops":aged_pops, "proportional_pops":proportional_pops, "indices":indices}

        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            value = values[queried_value][i]
            PointIndicator((x,y), value, pointIndicatorGroup)

    if dataset == "test":
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

        # normalise
        for i in range(len(xs)):
            x = (xs[i] - max_x) / (max_x - min_x)
            y = -(ys[i] - max_y) / (max_y - min_y)
            # print(x, y)
            x *= map_width
            y *= map_height
            x += width
            if (not names[i] in ("TOPLEFT", "BOTTOMRIGHT")):
                pi = PointIndicator((x,y), 1, pointIndicatorGroup)
                text_to_render.append((names[i], (x, y)))
    
    return pointIndicatorGroup

