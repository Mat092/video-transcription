# Lezioni NLP

this project aim is to create a simple package to trascribe video lessons from mp4 to docx file using google speech recognition

## TODO

- [x] A class for VideoToWav
- [x] A class for Splitting wav files into smaller ones
- [x] A class for the speech to txt recognizer
- [x] A class for the txt to docx transformation
- [x] Requirements
- [x] Setup
- [ ] Testing with github workflows
- [ ] Test for window
- [ ] Other fun things, like codequality and codecoverage

## Outline

MP4 files -> WAV Files -> SPLITTER -> Recognizer in txt -> 1 docx file per video

## Installation

Clone this repository into your system and install requirements and install

```bash
git clone https://github.com/Mat092/video-transcription.git
cd video-transcription
pip install -r requirements.txt
python setup.py install
```

## Usage

The simple script in (Example)[example/transcriptor.py] will trascribe to docx every file in inputdir:

```python
import video_transcription as vt

inputdir = 'path/to/video/directory'
tempdir = 'name/of/temporary/directory'

v2w = vt.VideoToWav(inputdir=inputdir)
v2w.extract_all_audios()

swa = vt.SplitWavAudio(inputdir=tempdir)
swa.split_all(min_per_split=2)

w2t = vt.WavToTxt(inputdir=tempdir)
w2t.transcribe_all()

t2d = vt.TxtToDoc(inputdir=tempdir)
t2d.convert()

```
