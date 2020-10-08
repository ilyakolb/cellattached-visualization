# -*- coding: utf-8 -*-

# batch create imaging/ephys combined videos
from make_cellattached_video import make_video
import os
import pandas as pd
from utils import find_directories

sensor_list = {'7f'}# {'686', '688', '456', 'XCaMP', '7f'}
main_movieout_dir = 'F:\jgcamp8_movies\output'
ephys_basedir = r'Z:\rozsam\raw\ephys'
vis_stim_basedir = r'Z:\rozsam\raw\visual_stim'
suite2p_basedir = r'Z:\rozsam\suite2p'

for sensor in sensor_list:
    table = pd.read_excel('movies_list.xlsx', sensor)
    for i,row in table.iterrows():
        print(i)
        stream_f, h5_f, vis_f, movie_f = find_directories(row, ephys_basedir, vis_stim_basedir, suite2p_basedir)
  

vis_stim_file_dir = r'Z:\rozsam\raw\visual_stim\20200831-anm479116\Cell3_Run03\31-Aug-2020_11_51_11_03.mat'
h5_file_dir = r'Z:\rozsam\raw\ephys\20200831-anm479116\Cell3\cell3_stim03_0001.h5'

'''
stream_file_dir = r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0\reg_tif\combo_square_adjLUT.tif'
movie_write_dir = r'F:/jgcamp8_movies/test.mp4'
dFF_file_dir = os.path.join(r'Z:\rozsam\suite2p\20200831-anm479116\Cell3\cell3_stim03_00001\plane0', 'dFF.npy')
'''
# make_video(stream_file_dir, h5_file_dir, vis_stim_file_dir, dFF_file_dir, movie_write_dir, start_frame = 2450, n_frames = 300, write_movie_fps = 30)



'''
DIR WITH MOVIE
# 20200831-anm479116/Cell3/cell3_stim03_00001/plane0/reg_tif/

session = '20200831'
subject = '479116'
cell =    '3'
runnum =  [3]
roi_num = [1]
'''
