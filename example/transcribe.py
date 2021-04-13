#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

import video_transcription as vt

__author__ = ['Mattia Ceccarelli']
__email__ = ['mattia.ceccarelli5@unibo.it']


def parse_args():

    description = 'This script transcribe every video in inputdir into docx file'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--inputdir', '--i',
                        dest='inputdir',
                        required=True,
                        type=str,
                        action='store',
                        help='datafile wher the video lessons are stored'
                        )

    parser.add_argument('--output', '--o',
                        dest='output',
                        required=False,
                        type=str,
                        action='store',
                        help='name of the output file in docx format',
                        default=''
                        )

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_args()

    inputdir = args.inputdir
    tempdir = os.path.join(inputdir, 'audio')

    v2w = vt.VideoToWav(inputdir=inputdir)
    v2w.extract_all_audios()

    swa = vt.SplitWavAudio(inputdir=tempdir)
    swa.split_all(min_per_split=2)

    w2t = vt.WavToTxt(inputdir=tempdir)
    w2t.transcribe_all()

    t2d = vt.TxtToDoc(inputdir=tempdir)
    t2d.convert()

    # os.rmdir(tempdir)
