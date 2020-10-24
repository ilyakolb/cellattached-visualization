# -*- coding: utf-8 -*-


# batch create imaging/ephys combined videos
from make_cellattached_video import make_video
import pandas as pd
import os
from utils import find_directories

preview = True # True to enable preview mode (2 secs of video)
sensor_list = {'686'}# {'686', '688', '456', 'XCaMP', '7f'}
main_movieout_dir = 'F:\jgcamp8_movies\output'
ephys_basedir = r'Z:\rozsam\raw\ephys'
vis_stim_basedir = r'Z:\rozsam\raw\visual_stim'
suite2p_basedir = r'Z:\rozsam\suite2p'

for sensor in sensor_list:
    table = pd.read_excel('movies_list.xlsx', sensor)
    for i,row in table.iterrows():
        if row['ignore']:
            print('Ignoring row {}'.format(i))
        else:
            print(i)
            stream_f, h5_f, vis_f, dff_f, movie_f = find_directories(row, ephys_basedir, vis_stim_basedir, suite2p_basedir, preview, sensor)
            
            if not stream_f or not h5_f or not vis_f or not dff_f:
                print('Skipping!')
            else:
                full_movie_file = os.path.join(main_movieout_dir, movie_f)
                make_video(stream_f, h5_f, vis_f, dff_f, full_movie_file, start_s = row['start s'], end_s = row['end s'], write_movie_fps = 30, preview_mode = preview)

'''
DIR WITH MOVIE
# 20200831-anm479116/Cell3/cell3_stim03_00001/plane0/reg_tif/

session = '20200831'
subject = '479116'
cell =    '3'
runnum =  [3]
roi_num = [1]
'''
