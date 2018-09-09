import math
import utm

# https://stackoverflow.com/questions/16266809/convert-from-latitude-longitude-to-x-y
CENTRAL_MERIDIAN = 149.75 # estimate of the central meridian of the canberra map, in degrees
COS_OF_MERIDIAN = math.cos(math.radians(CENTRAL_MERIDIAN))
EARTH_RADIUS = 6353 #km
def equirectangular_projection(lat, long):
    x = EARTH_RADIUS*long*COS_OF_MERIDIAN*EARTH_RADIUS
    y = EARTH_RADIUS*lat
    return x, y

# project from long, lat into cartesian coordinates
# def lat_long_to_x_y(lat, long):
#     # 35.10, 148.55 latlong is xy on 2160 map 173, 384
#     offset_x, offset_y = equirectangular_projection(35.10, 148.55)
#     x,y = equirectangular_projection(lat, long)
#     x += 5198958070
#     y += 224116
#     print(x,y)
#     return x, y

def lat_long_to_x_y(lat, long):
    x,y,_,_ = utm.from_latlon(lat, long)
    return x, y

# # convert lat/long to centidecimal representations (just for the minutes)
# # hacky as we only consider the minutes, but this isn't airflight software
# def sexagesimal_to_decimal(sexa):
#     minutes = sexa - math.ceil(sexa)
#     return math.ceil(sexa) + minutes/0.6

# # convert lat long to x,y
# # considering lat and long as an orthogonal grid as our map is so small
# def lat_long_to_x_y(lat, long):
#     # at these points these (x,y) match the corresponding 
#     # (lat, long) for the 2160*2160 map (determined in gimp)
#     # TOP_RIGHT_X_Y = 1712, 383
#     # BOTTOM_LEFT_X_Y = 558, 1799
    
#     # (lat, long) for the 1000*1000 map (determined in gimp)
#     # TOP_RIGHT_X_Y = 793, 173
#     # BOTTOM_LEFT_X_Y = 258, 813

#     TOP_RIGHT_X_Y = 793, 173
#     TOP_RIGHT_LAT_LONG = -35.10, 149.15

#     BOTTOM_LEFT_X_Y = 258, 813
#     BOTTOM_LEFT_LAT_LONG = -35.25, 149

#     # get lat,long in decimal terms
#     tr_ll = tuple(map(sexagesimal_to_decimal, TOP_RIGHT_LAT_LONG))
#     bl_ll = tuple(map(sexagesimal_to_decimal, BOTTOM_LEFT_LAT_LONG))

#     # normalise inputs
#     lat -= bl_ll[0]
#     long -= bl_ll[1]

#     lat_ratio = lat/(tr_ll[0]-bl_ll[0])
#     long_ratio = long/(tr_ll[1]-bl_ll[1])

#     print(lat_ratio)
#     print(long_ratio)

#     x = TOP_RIGHT_X_Y[0]*lat_ratio + BOTTOM_LEFT_X_Y[0]*(1-lat_ratio)
#     y = TOP_RIGHT_X_Y[1]*long_ratio + BOTTOM_LEFT_X_Y[1]*(1-long_ratio)

#     print(x)
#     print(y)
#     print()

#     return y, x