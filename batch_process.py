# -*- coding: utf-8 -*-

# batch create imaging/ephys combined videos
from make_cellattached_video import make_video
import os


vis_stim_file_dir = r'Z:\rozsam\raw\visual_stim\20200831-anm479116\Cell3_Run03\31-Aug-2020_11_51_11_03.mat'
h5_file_dir = r'Z:\rozsam\raw\ephys\20200831-anm479116\Cell3\cell3_stim03_0001.h5'

stream_file_dir = r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0\reg_tif\combo_square_adjLUT.tif'
movie_write_dir = r'F:/jgcamp8_movies/test.mp4'
dFF_file_dir = os.path.join(r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0', 'dFF.npy')

make_video(stream_file_dir, h5_file_dir, vis_stim_file_dir, dFF_file_dir, movie_write_dir, start_frame = 2450, n_frames = 300, write_movie_fps = 30)
