#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from time import time
from glob import glob
from tqdm import tqdm


__author__ = ['Mattia Ceccarelli']
__email__ = ['mattia.ceccarelli5@unibo.it']


class VideoToWav(object):
    '''
    This object is useful to extract multiple wav audio files from a collection of mp4 videos.
    1 audio file for every video into inputdir.

    Parameters
    ----------

    inputdir: string
      name of the directory containing the mp4 files to convert into wav audio

    outdir: string, optional
      name of the directory in which to save every wav audio file.
      If it doesn't exist, it will be created.
      If None, it will be initialized as 'inputdir/audio/'

    References
    ----------
    - https://becominghuman.ai/how-to-generate-text-from-a-video-file-using-python-261f59e95b5f
    '''

    def __init__(self, inputdir, outdir=None):

        self.inputdir = inputdir

        if outdir is None:
            self.outdir = os.path.join(inputdir, 'audio')

        else:
            self.outdir = outdir

        # TODO: add multiple format other than mp4
        self.filenames = glob(os.path.join(self.inputdir, '*.mp4'))

        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)

    @property
    def num_of_videos(self):
        return len(self.filenames)

    def mp3towav(self, filemp3, filewav, deletemp3=False):
        '''
        This function transform an mp3 file into a wav file.

        Parameters
        ----------

        filemp3: string
          path to the mp3 input file

        filewav:
          save path for the mp4 output file

        deletemp3: boo, default False
          wheter to delete the input mp3 file after the conversion or not

        '''

        command2wav = f'ffmpeg -i {filemp3} {filewav} -loglevel quiet'
        os.system(command2wav)

        if deletemp3:
            os.remove(filemp3)

    def mp4tomp3(self, filemp4, filemp3, deletemp4=False):
        '''
        This function transform an mp4 file into an mp3 file.

        Parameters
        ----------

        filemp4: string
          path to the mp4 input file

        filemp3:
          save path for the mp3 output file

        deletemp3: bool, default False
          wheter to delete the input mp4 file after the extraction or not
        '''

        command2mp3 = f'ffmpeg -i {filemp4} {filemp3} -loglevel quiet'
        os.system(command2mp3)

        if deletemp4:
            os.remove(filemp4)

    def mp4towav(self, filemp4, filewav):
        '''
        This function extract a single audio file from a single video using os and ffmpeg.

        Paramters
        ---------

        filemp4: string
          input video file in mp4 format

        filewav: string
          output wav file name
        '''

        filemp3 = os.path.join(self.outdir, 'audio.mp3')

        self.mp4tomp3(filemp4, filemp3, deletemp4=False)
        self.mp3towav(filemp3, filewav, deletemp3=True)

    def extract_all_audios(self):
        '''
        Extract a wav audio file from every .mp4 file into "inputdir" using os
        and ffmpeg, and save it into "outdir", with the same name of the video but with the format
        .wav
        '''

        start = time()

        pbar = tqdm(enumerate(self.filenames))
        for i, filepath in pbar:
            pbar.set_description(f'Exporting {self.num_of_videos} videos to wav')

            filename = filepath.split(os.path.sep)[-1].split('.')[0]
            filewav = os.path.join(self.outdir, filename + '.wav')
            self.mp4towav(filepath, filewav)

        print(f'Finished extracting {self.num_of_videos} files, it took {time() - start:.3}s')
