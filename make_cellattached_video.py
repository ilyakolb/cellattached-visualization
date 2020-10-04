# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 21:50:21 2020

@author: kolbi

real-time frame grabbing

INSTRUCTIONS
    Need to have ImageMagick Installed
    Run this with suite2p_backup conda environment (due to pyWavesurfer compatibility issues)

@todo:
    - add spike trace
    - enable movie slow-down or speed-up
    - aesthetics
    - vertical line at 0
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import os
import tifffile as tif
import warnings
from utils_ephys import extract_tuning_curve
plt.close('all')

start_frame = 500 # start at this frame index
dpi = 50
n_frames = 50 # num frames to write
write_movie_fps = 10 # fps of resulting movie (SHOULD = MOVIE FRAMERATE?)

x_lim = (-1,1)
y_lim = (-1,3)  # @todo: determine automatically?


vis_stim_file = r'Z:\rozsam\raw\visual_stim\20200831-anm479116\Cell3_Run03\31-Aug-2020_11_51_11_03.mat'
h5_file = r'Z:\rozsam\raw\ephys\20200831-anm479116\Cell3\cell3_stim03_0001.h5'

movie_dir = r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0'
movie_write_dir = 'F:/jgcamp8_movies/test.mp4'

dff_file = os.path.join(movie_dir, 'dFF.npy')

ephys_out = extract_tuning_curve(h5_file, vis_stim_file)
ephys_t_s = ephys_out['ephys_t']
ophys_t_s = ephys_out['frame_times']
dFF = np.load(dff_file)
ophys_sRate =  1/np.mean(np.diff(ophys_t_s))
ephys_sRate = 1/np.mean(np.diff(ephys_t_s))
end_frame = start_frame + n_frames
start_s, end_s = np.array([start_frame, end_frame])/ophys_sRate


# combined and cropped tif file of cell-attached recording
stream = tif.imread(os.path.join(movie_dir,'reg_tif', 'combo_square.tif'))
# stream = tif.imread(r'F:\jgcamp8_movies\sample\combined.tif')

# remove z axis (artifact of fiji import)
stream = stream.reshape((stream.shape[0]*stream.shape[1], stream.shape[2],stream.shape[3]))

if stream.shape[1] != stream.shape[2]:
    warnings.warn("WARNING: stream image is not square!")


fig = plt.figure()
ax1,ax2 = fig.subplots(1,2)
ax1.imshow(stream[0,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
ax1.axis("off")

line, = ax2.plot([], [], 'k-', lw=2)
ax2.plot([0, 0], y_lim, 'r--', lw=1) # vertical red line
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.set_xlim(x_lim)
ax2.set_ylim(y_lim)
ax2.set_aspect((x_lim[1]-x_lim[0]) / (y_lim[1]-y_lim[0])) # make sure plot is square, should be xlim / ylim

FFwriter = animation.FFMpegWriter(fps=write_movie_fps, extra_args=['-vcodec', 'libx264'])

frame_iter = range(start_frame, end_frame)

# set ImageMagick directory
ff_path = os.path.join('C:/', 'ImageMagick-7.0.10-Q16-HDRI', 'ffmpeg.exe')
plt.rcParams['animation.ffmpeg_path'] = ff_path

# always playing movie @30 FPS
# @todo: may need to address case where write_movie_fps != recording fps

# indices_to_shift = np.where(ephys_t_s <= 1/ophys_sRate,1,0).sum() # how many indices to shift every movie frame

with FFwriter.saving(fig, movie_write_dir, dpi):
    for i, frame_i in enumerate(frame_iter):
        ax1.imshow(stream[frame_i,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
        
        x = ophys_t_s - ophys_t_s[start_frame]
        y = np.roll(dFF, -1*i)
        line.set_data(x, y)
        FFwriter.grab_frame()
        print("done grabbing frame {}".format(i))
    print('DONE')
# plt.show()
