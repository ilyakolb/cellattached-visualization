# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 21:50:21 2020

@author: kolbi

real-time frame grabbing

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import os
import tifffile as tif

def make_square_axes(ax):
    """Make an axes square in screen units.

    Should be called after plotting.
    """
    ax.set_aspect(1 / ax.get_data_ratio())

plt.close('all')
stream = tif.imread(r'F:\jgcamp8_movies\sample\combined.tif')

# remove z axis (artifact of fiji import)
stream = stream.reshape((stream.shape[0]*stream.shape[1], stream.shape[2],stream.shape[3]))

movie_write_dir = r'F:\jgcamp8_movies\sample\test.mp4'
n_frames = 1000 # num frames to write
# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax1,ax2 = fig.subplots(1,2)
ax1.imshow(stream[0,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
ax1.axis("off")

line, = ax2.plot([], [], lw=2)
ax2.set_xlim(0,2)
ax2.set_ylim(-2,2)
ax2.set_aspect(1/2)
# ax2.axis("square")
# ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))


# plt.tight_layout()
plt.show()


FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
with FFwriter.saving(fig, movie_write_dir, n_frames):
    for i in range(n_frames):
        ax1.imshow(stream[i,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        FFwriter.grab_frame()


'''
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
'''
'''
def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,
'''
# call the animator.  blit=True means only re-draw the parts that have changed.
# anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

# need these
ff_path = os.path.join('C:/', 'ImageMagick-7.0.10-Q16-HDRI', 'ffmpeg.exe')
plt.rcParams['animation.ffmpeg_path'] = ff_path

# FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
# anim.save('basic_animation.mp4', writer = FFwriter)
# s = anim.to_html5_video()
# with open("myvideo.html", "w") as f:
#     print(anim.to_html5_video(), file=f)
# 