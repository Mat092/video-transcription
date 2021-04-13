#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from time import time
from tqdm import tqdm
from glob import glob

from docx import Document


__author__ = ['Mattia Ceccarelli']
__email__ = ['mattia.ceccarelli5@unibo.it']


class TxtToDoc(object):
    '''
    This object collects all txt files into a directory and convert them into a single
    docx file

    Parameters
    ----------

    inputdir: string
      input directory containing the txt files which will be converted into a single docx

    outfile: string
      path to the file which will be created (or substituted if already existing)

    Reference
    ---------
    - https://pythonprogramming.altervista.org/how-to-transfrom-a-txt-file-in-a-doc-file/
    '''

    def __init__(self, inputdir):
        self.inputdir = inputdir
        self.filenames = glob(os.path.join(self.inputdir, '*.txt'))

    @property
    def num_of_txt(self):
        return len(self.filenames)

    def convert(self):

        start = time()
        doc = Document()

        for i, file in tqdm(enumerate(self.filenames)):

            name = file.split(os.path.sep)[-1].split('.')[0]

            with open(file, 'r', encoding='utf-8') as openfile:
                line = openfile.read()
                doc.add_paragraph(line)
                doc.save(os.path.join(self.inputdir, '..', name + '.docx'))

        print(f'Finished converting {self.num_of_txt} into docx, it took {time() - start:.3}s')
