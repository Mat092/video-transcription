#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import math

from time import time
from tqdm import tqdm
from glob import glob

from pydub import AudioSegment


__author__ = ['Mattia Ceccarelli']
__email__ = ['mattia.ceccarelli5@unibo.it']


class SplitWavAudio():
    '''
    This class split wav file into smaller audio files

    Parameters
    ----------

    inputdir: string
      path to the wav file directory to split

    outputdir: string
      path to the inpudir where the new splitted wav files will be saved

    Reference
    ---------
    - https://stackoverflow.com/a/62872679
    '''

    def __init__(self, inputdir):
        self.inputdir = inputdir
        self.filenames = glob(os.path.join(inputdir, '*.wav'))

    def get_duration(self):
        return self.audio.duration_seconds

    @property
    def num_of_audios(self):
        return len(self.filenames)

    def single_split(self, from_min, to_min, savepath):
        '''
        This function separate a single split of the original wav file

        Parameters
        ----------

        from_min: int
          starting minute

        to_min: int
          ending minute

        split_filename: string
          name of this split
        '''

        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(savepath, format='wav')

    def multiple_split(self, min_per_split, file, deletewav=False):
        '''
        This function separate a file audio into multiple split

        Parameters
        ----------

        min_per_split: int
          lenght in minute of every split
        '''

        self.audio = AudioSegment.from_wav(file)
        total_mins = math.ceil(self.get_duration() / 60)

        name = file.split(os.path.sep)[-1].split('.')[0]
        savedir = os.path.join(self.inputdir, name)

        if not os.path.exists(savedir):
            os.mkdir(savedir)

        for i, minute in enumerate(range(0, total_mins, min_per_split)):

            savepath = os.path.join(savedir, f'{i:03}.wav')
            self.single_split(minute, minute + min_per_split, savepath)

        if deletewav:
            os.remove(file)

    def split_all(self, min_per_split):

        start = time()
        pbar = tqdm(self.filenames)
        for file in pbar:
            pbar.set_description(f'Splitting {self.num_of_audios} audios')
            self.multiple_split(min_per_split, file, deletewav=True)

        print(f'All splitted successfully, it took {time() - start:.3}s')
