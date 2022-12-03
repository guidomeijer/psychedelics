#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:17:41 2022
By: Guido Meijer
"""

import os
import numpy as np
import pandas as pd
from os.path import join, isdir, split, isfile
from glob import glob

# Settings
MODEL_PATH = '/home/guido/Data/SLEAP/OpenFieldCatheter/models/221201_174607.single_instance.n=102'
DATA_PATH = '/media/guido/Data2/Psychedelics/OpenField/Videos'
RESULT_PATH = '/home/guido/Dropbox/Work/Data/Psychedelics/OpenField/Tracking'

# Find videos to process
top_level_folders = glob(join(DATA_PATH, '*'))
for i, top_folder in enumerate(top_level_folders):
    if not isdir(join(RESULT_PATH, split(top_folder)[-1])):
        os.mkdir(join(RESULT_PATH, split(top_folder)[-1]))
    sub_folders = glob(join(DATA_PATH, top_folder, '*'))
    for j, sub_folder in enumerate(sub_folders):
        if not isdir(join(RESULT_PATH, split(top_folder)[-1], split(sub_folder)[-1])):
            os.mkdir(join(RESULT_PATH, split(top_folder)[-1], split(sub_folder)[-1]))
        video_files = glob(join(DATA_PATH, sub_folder, '*.avi'))
        for k, video_file in enumerate(video_files):
            output_path = join(RESULT_PATH, split(top_folder)[-1], split(sub_folder)[-1],
                               split(video_file)[-1][:-4])

            print(output_path)

            if not isfile(output_path + '.slp'):
                # Run SLEAP tracking
                print('Starting SLEAP tracking..')
                os.system((f'sleap-track --model {MODEL_PATH} '
                           f'--output {output_path} '
                           '--tracking.tracker flow '
                           f'{video_file}'))

            if not isfile(output_path + '.h5'):
                # Convert to H5 file format
                print('Converting output to .h5 file format..')
                os.system((f'sleap-convert -o {output_path + ".h5"} '
                           f'--format analysis '
                           f'{output_path + ".slp"}'))

            if not isfile(output_path + '_timestamps.npy'):
                # Convert to H5 file format
                meta_data = pd.read_csv(video_file[:-4] + '.csv', header=None)
                np.save(output_path + '_timestamps.npy', meta_data[1].values)

                print('Converting output to .h5 file format..')
                os.system((f'sleap-convert -o {output_path + ".h5"} '
                           f'--format analysis '
                           f'{output_path + ".slp"}'))

            # Compress video
            if not isfile(f'{video_file[:-4]}.mp4'):
                print('Compressing video..')
                os.system(f'ffmpeg -i {video_file} -c:v libx264 -crf 21 {video_file[:-4]}.mp4')

            # Delete original avi file
            # TO DO


