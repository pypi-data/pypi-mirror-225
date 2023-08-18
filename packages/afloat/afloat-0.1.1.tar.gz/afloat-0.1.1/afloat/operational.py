#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:33:59 2019

@author: andrewzulberti
"""

import numpy as np 
import matplotlib.pyplot as plt
import scipy.optimize
import utm

import gpxpy
import gpxpy.gpx

def triangulate(x, 
                y, 
                ranges, 
                total_depth,
                responder_height,
                x_drop=None,
                y_drop=None, 
                name='Unnamed object', 
                coord_sys='latlon'):

    def get_circle(xc, yc, r):
    
        xs = np.arange(xc-(r-tol), xc+(r-tol), 0.01)
        ysq = np.power(r, 2) - np.power((xs-xc), 2)
        ys = np.sqrt(ysq) + yc
        ys_ = -np.sqrt(ysq) + yc

        ys = np.concatenate((ys, ys_, (ys[0],)), 0)
        xs = np.concatenate((xs, np.flip(xs, 0), (xs[0],)), 0)

        return xs, ys
    
    def calculate_distance(checkparams, verbose = False):
        
        xcheck = checkparams[0]
        ycheck = checkparams[1]

        d1 = np.min(np.sqrt((y1 - ycheck)**2 ++ (x1 - xcheck)**2))
        d2 = np.min(np.sqrt((y2 - ycheck)**2 ++ (x2 - xcheck)**2))
        d3 = np.min(np.sqrt((y3 - ycheck)**2 ++ (x3 - xcheck)**2))
        d = np.sqrt(d1**2 + d2**2 + d3**2)

        if verbose:
            print('Distance 1 is {0}'.format(d1))
            print('Distance 2 is {0}'.format(d2))
            print('Distance 3 is {0}'.format(d3))

            print('Total distance is {0}'.format(d))

        return d

    tol = 0.1 
    lex = 700 # Width of the final plot

    vert_disp = - responder_height

    assert(len(x)==len(y))
    assert(len(x)==len(ranges))
    assert(len(x)>=3)
    
    got_drop=False
    if not y_drop is None:
        if not x_drop is None:
            got_drop=True
            
    if coord_sys == 'latlon':
        if got_drop:
            x_drop, y_drop, zone1, zone2 = utm.from_latlon(y_drop, x_drop)

        for ii, (xi, yi) in enumerate(zip(x, y)):#np.arange(0, len(x_extra)):
            x[ii], y[ii], zone1, zone2 = utm.from_latlon(y[ii], x[ii])

    print('UTM Zone: {0:.0f}, {1:s}'.format(zone1, zone2)) 
    # print(zone1)
    # print(zone2)

    # Only triangulates ont the first 3...
    r1 = np.sqrt(np.power(ranges[0], 2) - np.power(vert_disp, 2))
    r2 = np.sqrt(np.power(ranges[1], 2) - np.power(vert_disp, 2))
    r3 = np.sqrt(np.power(ranges[2], 2) - np.power(vert_disp, 2))

    # ... others are 'extra' and are plotted but not used
    ranges_extra = ranges[3::]
    x_extra = x[3::]
    y_extra = y[3::]
    
    x1, y1 = get_circle(x[0], y[0], r1)
    x2, y2 = get_circle(x[1], y[1], r2)
    x3, y3 = get_circle(x[2], y[2], r3)

    fig, axes = plt.subplots(nrows=1, figsize=(10, 10))

    axes.set_xlabel('Easting (m)')
    axes.set_ylabel('Northing (m)')
    
    r3h, = plt.plot(x3, y3, 'g', label='Third Mark')
    r2h, = plt.plot(x2, y2, 'r', label='Second Mark')
    r1h, = plt.plot(x1, y1, 'b', label='First Mark')

    if got_drop:
        axes.set_xlim((x_drop-lex, x_drop+lex))
        axes.set_ylim((y_drop-lex, y_drop+lex))
        ph, = plt.plot(x_drop, y_drop, 'kx', label='Drop Marker')
    
    print('There are {} extra points'.format(len(y_extra)))
    for ii in np.arange(0, len(y_extra)):

        re = np.sqrt(np.power(ranges_extra[ii], 2) - np.power(vert_disp, 2))

        xe, ye = get_circle(x_extra[ii], y_extra[ii], re)
        plt.plot(xe, ye, 'k--', label='Extra Marks')

    if len(y_extra)>0:

        re = np.sqrt(np.power(ranges_extra[ii], 2) - np.power(vert_disp, 2))

        xe, ye = get_circle(x_extra[ii], y_extra[ii], re)
        plt.plot(xe, ye, 'r:', label='Most recent mark Marks')


#     calculate_distance([x_drop, y_drop])

    fh = lambda pos: calculate_distance(pos)

    if got_drop:
        print('Initial guess taken as drop location.')
        x0 = [x_drop, y_drop]
    else:
        print('Initial guess taken as average of all marks, regardless of range.')
        x0 = [np.mean(x), np.mean(y)]
        print(x0)
        
    locale = scipy.optimize.fmin(func=fh, x0=x0)
    # lat, long = utm.to_latlon(locale[0], locale[1], 50, 'K')
    lat, long = utm.to_latlon(locale[0], locale[1], zone1, zone2)

    foundh, = plt.plot(locale[0], locale[1], 'gx', label='Solution')

#     if got_drop:
#         d = calculate_distance(locale, verbose = True)
#         textt = name + ': {0:.0f}, {1:.0f} [error: {2:.0f} m]'.format(locale[0], locale[1], d)
#         textt = name + ': {0:.5f}, {1:.5f} [error: {2:.0f} m]'.format(lat, long, d)
#     else:
#         textt = name + ': {0:.0f}, {1:.0f}'.format(locale[0], locale[1])
#         textt = name + ': {0:.5f}, {1:.5f}'.format(lat, long)
    d = calculate_distance(locale, verbose = True)
    textt = name + ': {0:.0f}, {1:.0f} [Uncertainty: {2:.0f} m]'.format(locale[0], locale[1], d)
    textt = name + ': {0:.5f}, {1:.5f} [Uncertainty: {2:.0f} m]'.format(lat, long, d)

    print(textt)
    plt.title(textt)

    plt.gca().set_aspect('equal', adjustable='box') 
    axes.grid(color='k', linestyle=':', linewidth=1, zorder=-1)

#     axes.legend([ph, r1h, r2h, r3h, foundh], ['Drop Marker', 'Range 1', 'Range 2', 'Range 3', 'Solution'])
#     axes.legend()
    handles, labels = axes.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axes.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))

    fullpathsave = '{name} Triangulation.png'.format(name=name)
    fig.savefig(fullpathsave)  
    
    return [lat, long], locale


class mygpx():
    """
    Parser/handler for GPX ship tracks which has seen very little testing. 
    """

    # Shouldn't import like this, but going for it!
    

    def __init__(self, gpxfgile):

        self.gpxfgile = gpxfgile
        self.read()
        self.process()
        
    def read(self):
        
        f = open(self.gpxfgile, 'r')
        print('File open')

        gpx = gpxpy.parse(f)
        print('File parsed')
        
        self.gpx = gpx
        
    def process(self):

        gpx_x = []
        gpx_y = []
        gpx_z = []
        gpx_t = []

        for track in self.gpx.tracks:
            for segment in track.segments:
                
                x = np.array([point.longitude for point in segment.points])
                y = np.array([point.latitude for point in segment.points])
                z = np.array([point.elevation for point in segment.points])
                t = np.array([point.time for point in segment.points])

                gpx_x += [x]
                gpx_y += [y]
                gpx_z += [z]
                gpx_t += [t]
                
        
        self.gpx_x = gpx_x
        self.gpx_y = gpx_y
        self.gpx_z = gpx_z
        self.gpx_t = gpx_t
        
        #         for point in segment.points:
        #             print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

        # for waypoint in gpx.waypoints:
        #     print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

        # for route in gpx.routes:
        #     print('Route:')
        #     for point in route.points:
        #         print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

# parse_solander_gpx(gpxfgile)
    def plot_gpx(self, plot_dict={}):

        for x, y in zip(self.gpx_x, self.gpx_y):
            plt.plot(x, y, linewidth=0.5, alpha=0.5)

        plt.gca().set_aspect('equal')
    