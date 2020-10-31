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

def make_video(stream_file_dir, h5_file_dir, vis_stim_file_dir, dFF_file_dir, movie_write_dir = "out.mp4", \
               start_s = 0, end_s = 2, dpi = 100, write_movie_fps = 30, speed = 1, invert_colors = False, preview_mode = True):
    '''
    make_video
    ----------
    create mp4 of Ca imaging and ephys side by side
    
    INPUTS:
        stream_file_dir: dir to combined tif file
        h5_file_dir: dir to wavesurfer h5 file
        vis_stim_file_dir: dir to visual stim file
        dFF_file_dir: dir to dFF.npy file
        movie_write_dir: mp4 file to write
        invert_colors (bool) # True for white on black background
        start_s (float)# start at this time
        end_s (float)# end at this time
        dpi (int) # output movie dpi
        write_movie_fps = 30 # fps of resulting movie
        speed (int) # set to 1 for regular speed, >1 for faster.
        preview_mode (bool): True to write a preview file where only e.g. 2 secs of video get recorded
        
    OUTPUTS:
        writes movie mp4 to movie_write_dir
    '''
    plt.close('all')
    
    if invert_colors:
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    if preview_mode:
        print("Preview mode on!")
        end_s = start_s + 4 # 2 seconds for preview
    
    ephys_out = extract_tuning_curve(h5_file_dir, vis_stim_file_dir)
    ephys_t_s = ephys_out['ephys_t']
    ophys_t_s = ephys_out['frame_times']
    ap_idx = ephys_out['ap_idx']
    dFF = np.load(dFF_file_dir)
    ophys_sRate =  1/np.mean(np.diff(ophys_t_s))
    start_frame, end_frame = np.array([int(start_s * ophys_sRate), int(end_s * ophys_sRate)])
    n_frames = end_frame - start_frame
    
    
    # combined and cropped tif file of cell-attached recording
    stream = tif.imread(stream_file_dir)

    # remove z axis (artifact of fiji import)
    stream = stream.reshape((stream.shape[0]*stream.shape[1], stream.shape[2],stream.shape[3]))
    
    if stream.shape[1] != stream.shape[2]:
        warnings.warn("WARNING: stream image is not square!")
    
    
    fig = plt.figure(figsize=[6,3])

    ax1,ax2 = fig.subplots(1,2)
    ax1.imshow(stream[0,:,:], extent=[0,100,0,1], aspect=100, cmap='gray') #, vmin=stream.min(), vmax=stream.max())
    ax1.axis("off")
    
    line, = ax2.plot(ophys_t_s - ophys_t_s[start_frame], dFF, 'w-' if invert_colors else 'k-', lw=2)
    ap_ticks, = ax2.plot(ephys_t_s[ap_idx],np.ones(len(ap_idx))*np.max(dFF)*-0.1,'r|', markersize=9, mew=2)
    stopwatch = ax2.text(0.65,0.9,'t = 0 s',ha='left', va='top', weight='bold', size=14, transform=ax2.transAxes)
    
    x_lim = (-1,1)
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
            ax1.imshow(stream[frame_i,:,:], extent=[0,100,0,1], aspect=100, cmap='gray', vmin=stream.min(), vmax=stream.max())
            
            # plot ophys trace
            line.set_xdata(ophys_t_s - ophys_t_s[frame_i])
            # plot AP markers
            ap_ticks.set_xdata(ephys_t_s[ap_idx] - ophys_t_s[frame_i])
            
            # update stopwatch
            stopwatch.set_text('t= {:.2f} s'.format(round(frame_i/ophys_sRate - ophys_t_s[start_frame], 2)))
            
            FFwriter.grab_frame()
            print("{}/{}: done grabbing frame {}".format(i+1, n_frames, frame_i))
        print('DONE')
