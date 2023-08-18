import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os, imageio, time

import datetime

from PIL import Image
import matplotlib.image as mpimg
from matplotlib import animation
import os, glob, afloat.plot.plotting as zplot

class gif_maker:
    """
    Simple tool for making animations from matplotlib figures. Fundamentally this is a gif maker - because it's simpler and more stable -but there is also mp4 support.
    
    USAGE:
        (1) initialise the gif_maker giving it a name for the gif [without extension] and a directory [default is '.']
            
                e.g.:
                    gm = gif_maker('Eta with quivers', '../../folder_to_save_gif')
                    
        (2) run some loop that creates your frames and pass the matplotlib figure handle to the gif_maker each time. 
            Note you can update the same figure continually or you can 
            
                e.g.:
                    for i in np.arange(0, nloops):
                        fig = plt.figure(figsize=(10, 8)) # Create the figure
                        
                        # SOME USER-DEFINED FUNCTION # SOME USER-DEFINED FUNCTION
                        update_figure(fig, i) # SOME USER-DEFINED FUNCTION
                        # SOME USER-DEFINED FUNCTION # SOME USER-DEFINED FUNCTION
                        
                        gm.capture_fig(fig) # This is the gif_maker capture step. It saves a png image to file and tracks 
                                              it for splicing into the gif atr a later stage
                                              
        (3) make the gif once the loop is complete. frame rate can be spoecified at this point.
        
                e.g.:
                    
                                              
    """
    def __init__(self, gif_name, gif_dir='.'):

        self.gif_name = gif_name
        
        if not os.path.exists(gif_dir):
            os.mkdir(gif_dir)

        gif_stills_dir = os.path.join(gif_dir, 'stills')
        if not os.path.exists(gif_stills_dir):
            os.mkdir(gif_stills_dir)

        self.gif_dir = gif_dir
        self.gif_stills_dir = gif_stills_dir
        
        self.stills = []
        
    def capture_fig(self, fig):
        """
        This function saves a matplotlib figure and tracks the output file for the animation production
        """

        still_number = len(self.stills)
        savename = os.path.join(self.gif_stills_dir, '{}{}.png'.format(self.gif_name, still_number))
        
        fig.savefig(savename)
        self.stills += [savename]
        pass
    
    def get_stills_from_dir(self):
        """
        This function will spit get stills from a folder and sort them by frame number.
        """
        
        stills = glob.glob(self.gif_stills_dir +'/'+self.gif_name+'*.png')

        print(len(stills))
        
        still_numbers = np.array([int(still[len(os.path.join(self.gif_stills_dir, self.gif_name)):-4]) for still in stills])
        ind = np.argsort(still_numbers)
        ind

        self.stills = np.array(stills)[ind]
    
    @property
    def gif_fullpath(self):
        
        return os.path.join(self.gif_dir, '{}{}'.format(self.gif_name, '.gif'))
    @property
    def mp4_fullpath(self):
        
        return os.path.join(self.gif_dir, '{}{}'.format(self.gif_name, '.mp4'))
    
    def make_gif(self, fps=5):
        
        with imageio.get_writer(self.gif_fullpath, mode='I', fps=fps) as writer:
            for still in self.stills:
                image = imageio.imread(still)
                writer.append_data(image)

    def make_mp4(self, start_frame=0, end_frame=10, frame_skip=1, fps=5, dpi=300, save_count=100):
        """
        Make an MP4 using matplotlib.


        """
        
        interval = int(1000/fps)
        files_sorted = self.stills
        
        frame_array = np.arange(start_frame, end_frame+1, frame_skip)
        frames = len(frame_array)
        
        im = Image.open(files_sorted[0])

        shape = im.size

        fig = plt.figure()
        al = zplot.axis_layer(left=0, right=0, top=0, bottom=0
                              , widths=[shape[0]/np.sqrt(dpi)]
                              , heights=[shape[1]/np.sqrt(dpi)])
        al.verbose = False
        al.lay(0, 0)

        # img = mpimg.imread(files[0])
        # imgplot = plt.imshow(img)

        #####################
        # DEFINE THE ANIMATOR
        #####################
        def animate(i):
        #     x = np.linspace(0, 2, 1000)
        #     y = np.sin(2 * np.pi * (x - 0.01 * i))
        #     line.set_data(x, y)
        #     return line,
        
            start = time.time()
            frame_no = frame_array[i]

            file = files_sorted[frame_no]
            print(files_sorted[frame_no])
            img = mpimg.imread(files_sorted[frame_no])
            imgplot = plt.imshow(img)
            # print("hello")
            
            end = time.time()
            print('   Time this frame: {}'.format(end - start))
            
            return [imgplot]


        ###################
        # CALL THE ANIMATOR
        ###################
        # call the animator.  blit=True means only re-draw the parts that have changed.
        # anim = animation.FuncAnimation(fig, animate, init_func=init,
        #                                frames=10, interval=20, blit=True)
        cache_frame_data = False
        anim = animation.FuncAnimation(fig, animate,
                                       frames=frames, interval=interval, blit=True,
                                       cache_frame_data = cache_frame_data,
                                       save_count=save_count)


        ####################
        # SAVE THE ANIMATION
        ####################
        # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        # anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
        
        # save_name = os.path.join(self.gif_dir, '{}{}'.format(self.gif_name, '.mp4'))
        save_name = self.mp4_fullpath

        anim.save(save_name, fps=fps)
        print('Saved ' + save_name)
        