# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 21:50:21 2020

@author: kolbi

real-time frame grabbing

INSTRUCTIONS
    Need to have ImageMagick Installed
    Run this with suite2p_backup conda environment (due to pyWavesurfer compatibility issues)

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import os
import tifffile as tif
import warnings
from utils_ephys import extract_tuning_curve
plt.close('all')

invert_colors = True # True for white on black background
start_frame = 2450 # start at this frame index
dpi = 100
n_frames = 100 # num frames to write
write_movie_fps = 30 # fps of resulting movie

speed = 1 # (int) set to 1 for regular speed, >1 for faster. speed > 1 results in jitteriness
x_lim = (-1,1)

if invert_colors:
    plt.style.use('dark_background')

vis_stim_file = r'Z:\rozsam\raw\visual_stim\20200831-anm479116\Cell3_Run03\31-Aug-2020_11_51_11_03.mat'
h5_file = r'Z:\rozsam\raw\ephys\20200831-anm479116\Cell3\cell3_stim03_0001.h5'

movie_dir = r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0'
movie_write_dir = 'F:/jgcamp8_movies/test.mp4'

dff_file = os.path.join(movie_dir, 'dFF.npy')

ephys_out = extract_tuning_curve(h5_file, vis_stim_file)
ephys_t_s = ephys_out['ephys_t']
ophys_t_s = ephys_out['frame_times']
ap_idx = ephys_out['ap_idx']
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

# downsample by 'speed' if needed
# stream = stream[::speed,:,:]

if stream.shape[1] != stream.shape[2]:
    warnings.warn("WARNING: stream image is not square!")


fig = plt.figure(figsize=[6,3])
# figure color
# fig.patch.set_facecolor('black' if invert_colors else 'white')
ax1,ax2 = fig.subplots(1,2)
ax1.imshow(stream[0,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
ax1.axis("off")

line, = ax2.plot(ophys_t_s - ophys_t_s[start_frame], dFF, 'w-' if invert_colors else 'k-', lw=2)
ap_ticks, = ax2.plot(ephys_t_s[ap_idx],np.ones(len(ap_idx))*np.max(dFF)*-0.1,'r|')
stopwatch = ax2.text(0.65,0.9,'t = 0 s',ha='left', va='top', weight='bold', size=14, transform=ax2.transAxes)

y_lim = (-1,dFF.max()+0.1)

ax2.plot([0, 0], y_lim, 'r--', lw=1.5) # vertical red line
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.set_xlim(x_lim)
ax2.set_ylim(y_lim)
ax2.set_aspect((x_lim[1]-x_lim[0]) / (y_lim[1]-y_lim[0])) # make sure plot is square, should be xlim / ylim
ax2.set_xlabel('Time (s)')
ax2.set_ylabel(r"$\Delta$F/F")
FFwriter = animation.FFMpegWriter(fps=write_movie_fps, extra_args=['-vcodec', 'libx264'])

frame_iter = range(start_frame, end_frame, speed)

# set ImageMagick directory
ff_path = os.path.join('C:/', 'ImageMagick-7.0.10-Q16-HDRI', 'ffmpeg.exe')
plt.rcParams['animation.ffmpeg_path'] = ff_path

plt.tight_layout()
with FFwriter.saving(fig, movie_write_dir, dpi):
    for i, frame_i in enumerate(frame_iter):
        
        # draw cell image
        ax1.imshow(stream[frame_i,:,:], extent=[0,100,0,1], aspect=100, cmap='gray')
        
        # plot ophys trace
        line.set_xdata(ophys_t_s - ophys_t_s[frame_i])
        # plot AP markers
        ap_ticks.set_xdata(ephys_t_s[ap_idx] - ophys_t_s[frame_i])
        
        # update stopwatch
        stopwatch.set_text('t= {} s'.format(round(frame_i/ophys_sRate - ophys_t_s[start_frame], 2)))
        
        FFwriter.grab_frame()
        print("{}/{}: done grabbing frame {}".format(i, n_frames, frame_i))
    print('DONE')
# plt.show()
