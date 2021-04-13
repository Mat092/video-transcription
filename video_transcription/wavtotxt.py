#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from time import time
from glob import glob
from tqdm import tqdm

import speech_recognition as sr


__author__ = ['Mattia Ceccarelli']
__email__ = ['mattia.ceccarelli5@unibo.it']


class WavToTxt(object):
    '''
    This object is used to create a txt file which is the transcription of the content in
    wav files. In doing so, it uses the speech_recognition library and in particular google speech
    speech recognition

    Parameters
    ----------

    inputdir: string
      directory in which wav files to transcribe and collect are stored

    txtfilename: string
      name of the txt file to create and store the wav audio transcription

    References
    ----------
    - https://becominghuman.ai/how-to-generate-text-from-a-video-file-using-python-261f59e95b5f
    - https://github.com/Uberi/speech_recognition
    '''

    def __init__(self, inputdir):

        self.inputdir = inputdir
        self.directories = glob(os.path.join(self.inputdir, '*[!.txt]'))
        self.missing = []

    @property
    def num_of_audios(self):
        return len(self.directories)

    def transcribe_all(self, language='it-IT'):
        '''
        This function trascribe all files into inputdir into different txt file
        using google speech recognition.

        Parameters
        ----------

        language: string, default 'it-IT'
          language of the audio: italian is 'it-IT', english 'en-UK' or 'en-US' etc...

        '''
        start = time()
        for i, dir in enumerate(self.directories):

            txtpath = dir + '.txt'

            with open(txtpath, 'a+') as txt:

                pbar = tqdm(sorted(glob(os.path.join(dir, '*.wav'))))
                for filewav in pbar:
                    pbar.set_description(f'Transcribing audios {i}/{self.num_of_audios}')

                    r = sr.Recognizer()
                    audio = sr.AudioFile(filewav)

                    with audio as source:
                        audio_data = r.record(source, duration=120)

                        text = f'Missing Audio {filewav}'
                        try:
                            text = r.recognize_google(audio_data, language=language)
                        except sr.UnknownValueError:
                            pass

                        if 'Missing' in text:
                            self.missing.append(text)

                        txt.write(text)
                        txt.write(' // ')

        print(f'Finished transcribing {self.num_of_audios}, it took {(time() - start) / 60:.3}min')
        print(self.missing)
