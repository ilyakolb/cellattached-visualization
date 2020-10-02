# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 21:50:21 2020

@author: kolbi

real-time frame grabbing

INSTRUCTIONS
    Need to have ImageMagick Installed
    Run this with suite2p_backup conda environment (due to pyWavesurfer compatibility issues)
@todo: online_ephys_analysis should make dff and spike struct
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
n_frames = 50 # num frames to write
write_movie_fps = 30 # fps of resulting movie (SHOULD = MOVIE FRAMERATE?)

vis_stim_file = r'Z:\rozsam\raw\visual_stim\20200831-anm479116\Cell3_Run03\31-Aug-2020_11_51_11_03.mat'
h5_file = r'Z:\rozsam\raw\ephys\20200831-anm479116\Cell3\cell3_stim03_0001.h5'

# load dff_and_spike struct in the form 'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0'
movie_dir = r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0'
movie_write_dir = 'F:/jgcamp8_movies/test.mp4'

dff_file = os.path.join(movie_dir, 'dFF.npy')

ephys_out = extract_tuning_curve(h5_file, vis_stim_file)
ephys_t_s = ephys_out['ephys_t']
ophys_t_s = ephys_out['frame_times']
dFF = np.load(dff_file)
frame_sRate =  1/np.mean(np.diff(ophys_t_s))
end_frame = start_frame + n_frames
start_s, end_s = np.array([start_frame, end_frame])/frame_sRate


# combined and cropped tif file of cell-attached recording
# stream = tif.imread(os.path.join(movie_dir,'reg_tif', 'combo.tif'))
stream = tif.imread(r'F:\jgcamp8_movies\sample\combined.tif')

# remove z axis (artifact of fiji import)
stream = stream.reshape((stream.shape[0]*stream.shape[1], stream.shape[2],stream.shape[3]))

if stream.shape[1] != stream.shape[2]:
    warnings.warn("WARNING: stream image is not square!")


fig = plt.figure()
ax1,ax2 = fig.subplots(1,2)
ax1.imshow(stream[0,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
ax1.axis("off")

line, = ax2.plot([], [], lw=2)


x_lim = (-2,2)
y_lim = (-1,3)  # @todo: determine automatically?

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
indices_to_shift = np.where(ephys_t_s <= 1/write_movie_fps,1,0).sum() # how many indices to shift every movie frame
with FFwriter.saving(fig, movie_write_dir, n_frames):
    for i, frame_i in enumerate(frame_iter):
        ax1.imshow(stream[frame_i,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
        
        x = ophys_t_s - ophys_t_s[start_frame] - i
        y = np.roll(dFF, i)
        line.set_data(x, y)
        FFwriter.grab_frame()
        print("done grabbing frame {}".format(i))
plt.show()


# mock data
'''
FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
with FFwriter.saving(fig, movie_write_dir, n_frames):
    for i in range(n_frames):
        ax1.imshow(stream[i,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        FFwriter.grab_frame()
'''
