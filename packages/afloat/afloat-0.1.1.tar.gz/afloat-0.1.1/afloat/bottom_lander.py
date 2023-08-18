"""
Various tools for working with bottom landers. Ultimately looking to have frame interference and :

Functions
=========
    - XXX:   XXX
    - XXX:   XXX

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import path as mplpath
import afloat 

strict = False # only way to get this to work with autoreload. 

def rectify_xy(x, y, theta, rotate):
    """
    Rotate arbitrary amount in x and y
    """
    
    if rotate:
        h = (np.pi/180)*-theta
    else:
        h = 0

    x_ =  x*np.cos(h) - y*np.sin(h)
    y_ =  x*np.sin(h) + y*np.cos(h)

    return x_, y_
       
class frame_obs:
    """
    Class for handling single instrument record. At the moment handles Nortek Signature and Nortek Vector only. 
    """

    name = 'Unnamed obs'
        
    x_offset = 0
    y_offset = 0
    z_offset = 0
    
    t = None
    u, v, w = None, None, None
    b1, b2, b3 = None, None, None
    
    x_axis_expected = 0 # X axis as expected when laying out frame. Must be noted in field notes. 
    
    heading_oem = 0 # Measured Heading in manufacturer coordinates
    pitch_oem   = 0 # Measured Pitch in manufacturer coordinates
    roll_oem    = 0 # Measured Roll in manufacturer coordinates
    
    known_instrs = ["signature", "sig", "vector", "vec"]
    _instr = 'signature'

    good_arcs = []
    bad_arcs = []
    arc_grow = 1.25

    title_loc='north'

    def __init__(self, name, x=0, y=0, z=0, x_axis_expected=0, heading_oem=0, u=None, v=None, w=None, **vargs):
        
        self.__dict__.update(**vargs)
        self.name = name
        
        self.x_offset = x
        self.y_offset = y
        self.z_offset = z
        
        self.x_axis_expected = x_axis_expected
        
        self.heading_oem = heading_oem
        
        self.upright = True
    
    def print_insrument_conventions(self):

        known = self.known_instrs
        instr = self.instr
        
        if instr.lower() in known:
            pass
        else:
            raise(Exception("Instrument mus be in {}".format(known)))

        print(instr+':')
        if instr.lower() in ["signature", "sig"]:
            print("  Heading is defined as the geogaphical direction of the 'x' axis")
            print("  The 'x' axis is defined as the geogaphical direction of BEAM 1")
            print("  Instrument is oriented 'up' if transducers are pointing up. ")

        if instr.lower() in ["vector", "vec"]:
            print("  Heading is defined as the geogaphical direction of the 'x' axis")
            print("  The 'x' axis is defined as the geogaphical direction of BEAM 1")
            print("  Instrument is oriented 'up' if the canister is above the transducers (transducers are pointing down). ")

    @property
    def instr(self):        
        
        instr = self._instr
        if instr.lower() in ["signature", "sig"]:
            instr = 'signature'

        if instr.lower() in ["vector", "vec"]:
            instr = 'vector'
        
        return instr
    
    # Define setter
    @instr.setter
    def instr(self, value):
        self._instr = value.lower()
        
    @property
    def beam_data(self):
        
        instr = self.instr
        
        if instr in ['vector']:
            beam_rots = [2*np.pi/3, 4*np.pi/3, 0]
            beam_names_if_up = ['B2', 'B3', 'B1', ]
            beam_names_if_down = ['B3', 'B2', 'B1', ]
        elif instr in ['signature']:
            # Just plot slanted beams
            beam_rots = [2*np.pi/4, 4*np.pi/4, 6*np.pi/4, 0]
            beam_names_if_up = ['B2', 'B3', 'B4', 'B1', ]
            beam_names_if_down = ['B3', 'B2', 'B4', 'B1', ]
        
        beam_names = beam_names_if_up
        if not self.upright:
            beam_names = beam_names_if_down
            
        return beam_rots, beam_names
    
        
    @property
    def axis_data(self):
        
        instr = self.instr
        
        if instr in ['vector']:
            rots_if_up = np.array([0, 1*np.pi/2])
            names = ['X', 'Y']
        elif instr in ['signature']:
            # Just plot slanted beams
            rots_if_up = np.array([0, 6*np.pi/4])
            names = ['X', 'Y']
      
        rots = rots_if_up
        if not self.upright:
            rots = -rots_if_up
            
        return rots, names
    
    def rotate(self, x, y, z):
        
        o = self
        p_oem, r_oem, h_oem, h_exp = o.pitch_oem, o.roll_oem, o.heading_oem, o.x_axis_expected
        
        h_oem = (np.pi/180)*(90-h_oem)
        h_exp = (np.pi/180)*(90-h_exp)
        
        p_oem = (np.pi/180)*(p_oem)
        r_oem = (np.pi/180)*(r_oem)
        
#         % Think these should be negative
        hh = -h_oem
        pp = -p_oem
        rr = -r_oem

        H = np.array([[np.cos(hh), np.sin(hh), 0],[ -np.sin(hh), np.cos(hh), 0],[0, 0, 1]])

        # % Make tilt matrix
        P = np.array([[np.cos(pp), -np.sin(pp)*np.sin(rr), -np.cos(rr)*np.sin(pp)],
             [0, np.cos(rr), -np.sin(rr)],  
             [np.sin(pp), np.sin(rr)*np.cos(pp),  np.cos(pp)*np.cos(rr)]])

        # % Make resulting transformation matrix
        xyz2enu = np.matmul(H, P)

        xyz = np.stack([x, y, z])

        enu = xyz2enu @ xyz

        x = enu[0, :]
        y = enu[1, :]
        z = enu[2, :]
        
        return x, y, z

    def plot(self, heading_length=200, frame_rotation=0):

        rotate_frame = True
        max_y = 0
        max_x = 0
        
        o = self
        x, y, z = o.x_offset, o.y_offset, o.z_offset
        p_oem, r_oem, h_oem, h_exp = o.pitch_oem, o.roll_oem, o.heading_oem, o.x_axis_expected
        
        if rotate_frame:
            h_exp += frame_rotation
    
        instr = o.instr
        upright = o.upright

        h_oem = (np.pi/180)*(90-h_oem)
        h_exp = (np.pi/180)*(90-h_exp)
        
        p_oem = (np.pi/180)*(p_oem)
        r_oem = (np.pi/180)*(r_oem)

        x, y = rectify_xy(x, y, frame_rotation, rotate_frame) 
        
        plt.plot(x, y, 'kx')

        # Plot expected heading
        hexp_x = heading_length*np.cos(h_exp)
        hexp_y = heading_length*np.sin(h_exp)
        
        xv = np.array([0, hexp_x])
        yv = np.array([0, hexp_y])
        
        plt.plot(x+xv, y+yv, 'b--', label='Instr. X expected')

        max_x = np.max([max_x, max(xv)])
        max_y = np.max([max_y, max(yv)])
        
        # Plot a circle
        t = np.linspace(0, 2*np.pi, 100);
        xc = np.cos(t)*heading_length/2
        yc = np.sin(t)*heading_length/2
        zc = t*0
        
        xc, yc, zc = self.rotate(xc, yc, zc)

        plt.plot(x+xc, y+yc, 'k--')
        plt.plot(x+xc[0], y+yc[0], 'k*')

        # Plot out all beams, ending with the 'Heading' beam
        beam_rots, beam_names = o.beam_data

        for br, bn in zip(beam_rots, beam_names):
            
#             hoem_x = heading_length*np.cos(h_oem+br)
#             hoem_y = heading_length*np.sin(h_oem+br)
            hoem_x = heading_length*np.cos(br)
            hoem_y = heading_length*np.sin(br)
        
            xv = np.array([0, hoem_x])
            yv = np.array([0, hoem_y])
            
            max_x = np.max([max_x, max(xv)])
            max_y = np.max([max_y, max(yv)])
            
            zv = yv*0
            
            xv, yv, zv = self.rotate(xv, yv, zv)
            
            plt.plot(x+xv, y+yv, '0.5', linestyle=':')

            plt.text(x+xv[-1], y+yv[-1], '  '+bn, fontsize='small')
            
        axis_rots, axis_names = o.axis_data

        for i, (ar, an) in enumerate(zip(axis_rots, axis_names)):
            
            if i==0:
                col = 'r'
            elif i==1:
                col = 'g'
            else:
                continue
                
            if an.lower()=='x':
                lab = 'Instr. X observed'
            elif an.lower()=='y':
                lab = 'Instr. Y observed'
            else:
                lab = None
                
            hoem_x = heading_length*np.cos(ar)
            hoem_y = heading_length*np.sin(ar)
        
            xv = np.array([0, hoem_x])
            yv = np.array([0, hoem_y])
            
            max_x = np.max([max_x, max(xv)])
            max_y = np.max([max_y, max(yv)])
            
            zv = yv*0
            
            xv, yv, zv = self.rotate(xv, yv, zv)
            
            plt.plot(x+xv, y+yv, col, linestyle='-', label=lab)

            plt.text(x+xv[-1], y+yv[-1], an+'  ', color=col, fontsize='small', ha='right', va='bottom')
            
#         plt.plot(x+xv, y+yv, 'r', label='OEM heading')
    
        def plot_arc(arc, col, lab):
    
            arcs = arc[0]
            arce = arc[1]
            
            assert(arcs<=arce)
                
            t = np.linspace(arcs, arce, 100);
            t = 90-t
            t *= np.pi/180
            grow = self.arc_grow 
            xc = np.hstack([np.cos(t)*heading_length*(grow)/2, np.cos(t[::-1])*heading_length/(grow*2)])
            yc = np.hstack([np.sin(t)*heading_length*(grow)/2, np.sin(t[::-1])*heading_length/(grow*2)])
            
            plt.fill(x+xc, y+yc, col, alpha=0.4, label=lab)
            
        
        for arc in self.good_arcs:

            plot_arc(arc, 'g', 'Frame interference: no')
            
        for arc in self.bad_arcs:

            plot_arc(arc, 'r', 'Frame interference: yes')
            
            plt.grid()
        
        plt.gca().set_aspect('equal')
        plt.grid('on')
        
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
        
        if self.title_loc.lower()=='north':
            plt.text(x, 1.1*max_y+y, '' + o.name + '\n[z=' + str(z) + ' mm]\n', ha='center', va='bottom', fontweight='bold')
        elif self.title_loc.lower()=='east':
            plt.text(1.1*max_x+x, y, '' + o.name + '\n[z=' + str(z) + ' mm]\n', ha='left', va='center', fontweight='bold')
        elif self.title_loc.lower()=='northeast':
            plt.text(max_x+x, max_y+y, '' + o.name + '\n[z=' + str(z) + ' mm]\n', ha='left', va='bottom', fontweight='bold')
        elif self.title_loc.lower()=='south':
            plt.text(x, -1.1*max_y+y, '' + o.name + '\n[z=' + str(z) + ' mm]\n', ha='center', va='top', fontweight='bold')
        elif self.title_loc.lower()=='west':
            plt.text(-1.1*max_x+x, y, '' + o.name + '\n[z=' + str(z) + ' mm]\n', ha='right', va='center', fontweight='bold')
        else:
            raise(Exception('Title location not recognised'))
        

    
class frame:
    obs = []
    
    frame_land_heading = 0
    
    # 2D Geometry of the frame. Default UWA Lander
    x = np.array([0, 1200, 2400])
    y = np.array([0, 2078, 0])
    
    a = np.sin(30*np.pi/180)*600/np.sin(60*np.pi/180)
    x_sub = [x/2+600]
    y_sub = [y/2+a]
    
    def init(self, x, y):
        obs = []
        self.x, self.y = x, y 
        
    def __validate__(self):
        for o in self.obs:
            print(type(o))

            if strict:
                assert(type(o)==frame_obs | type(o)==afloat.bottom_lander.frame_obs) # This fails with module autoreload
            else:
                pass
        
        print("This frame has {} observations".format(len(self.obs)))
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        """
        Custom print method
        """
        
        self.__validate__()
        
        return 'Not doing anything'
    
    def add_obs(self, o):
        
        if strict:
            assert(type(o)==frame_obs | type(o)==afloat.bottom_lander.frame_obs) # This fails with module autoreload
        else:
            pass

        self.obs.append(o)
        pass
    
    def draw_old(self, rotate_frame=True, figsize=(7, 7)):
        
        heading_length = 200
        
        plt.figure(figsize=figsize)
        
        plt.plot(0, 0, 'r+')
        
        max_y = 0
        for o in self.obs:
            
            x, y, z, h_oem, h_exp = o.x_offset, o.y_offset, o.z_offset, o.heading_oem, o.x_axis_expected
            instr = o.instr
            upright = o.upright
            
            if rotate_frame:
#                 h_oem += self.frame_land_heading
                h_exp += self.frame_land_heading

            h_oem = (np.pi/180)*(90-h_oem)
            h_exp = (np.pi/180)*(90-h_exp)
            
            x, y = rectify_xy(x, y, self.frame_land_heading, rotate_frame) 
            
            plt.plot(x, y, 'kx')
            plt.text(x, y, '   ' + o.name + ' [z=' + str(z) + ' mm]')
            
            # Plot expected heading
            hexp_x = heading_length*np.cos(h_exp)
            hexp_y = heading_length*np.sin(h_exp)
            xv = np.array([x, x+hexp_x])
            yv = np.array([y, y+hexp_y])
#             xv, yv = self.rectify_xy(xv, yv, rotate_frame)  

            plt.plot(xv, yv, 'b--', label='Expected heading')
            
            # Plot out all beams, ending with the 'Heading' beam
            beam_rots, beam_names_if_up = o.beam_data
            
            for br, bm in zip(beam_rots, beam_names_if_up):
                hoem_x = heading_length*np.cos(h_oem+br)
                hoem_y = heading_length*np.sin(h_oem+br)
                xv = np.array([x, x+hoem_x])
                yv = np.array([y, y+hoem_y])
                plt.plot(xv, yv, '0.5', linestyle=':')
                
                plt.text(xv[-1], yv[-1], bm)
                
            plt.plot(xv, yv, 'r', label='OEM heading')
                       
        # Now plot the frame
        x, y = self.x, self.y
        x, y = rectify_xy(x, y, self.frame_land_heading, rotate_frame) 
        plt.fill(x, y, 'k', alpha=0.05)
        
        for x, y in zip(self.x_sub, self.y_sub):
            x, y = rectify_xy(x, y, self.frame_land_heading ,rotate_frame) 
            
            plt.fill(x, y, 'k', alpha=0.05, ec='k', ls='-')
        
        plt.grid('on')
        plt.gca().set_aspect('equal')
        plt.xlabel('X offset (mm)')
        plt.ylabel('Y offset (mm)')
        
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        # plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
        plt.legend(by_label.values(), by_label.keys())
#         plt.legend()

        if rotate_frame:
            plt.title('Frame rotated as landed on seabed')
        else:
            plt.title('Assuming frame landed with nominal North')

        # plt.show()
        
        return plt.gcf()

    def draw(self, rotate_frame=True, figsize=(7, 7), heading_length=200):
        
        plt.figure(figsize=figsize)
        
        if rotate_frame:
            frame_rotation = self.frame_land_heading
        else:
            frame_rotation = 0
            
        plt.plot(0, 0, 'r+')
        
        for o in self.obs:
            
#             x, y = rectify_xy(x, y, rotate_frame) 
            o.plot(frame_rotation=frame_rotation, heading_length=heading_length)
            
        # Now plot the frame
        x, y = self.x, self.y
        x, y = rectify_xy(x, y, self.frame_land_heading, rotate_frame) 
        plt.fill(x, y, 'k', alpha=0.05)
        
        for x, y in zip(self.x_sub, self.y_sub):
            x, y = rectify_xy(x, y, self.frame_land_heading, rotate_frame) 
            
            plt.fill(x, y, 'k', alpha=0.05, ec='k', ls='-')
        
        plt.grid('on')
        plt.gca().set_aspect('equal')
        plt.xlabel('X offset (mm)')
        plt.ylabel('Y offset (mm)')
        
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        # plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
        plt.legend(by_label.values(), by_label.keys())

#         plt.legend()

        if rotate_frame:
            plt.title('Frame rotated as landed on seabed')
        else:
            plt.title('Assuming frame landed with nominal North')

        return plt.gcf()    