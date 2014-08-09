__author__ = 'emptysamurai'

import argparse
import re
import vad
from subrip import SubRip
from pathlib import PurePath


# parse arguments
parser = argparse.ArgumentParser(
    description="Generates SubRip (srt) subtitles for the given speech audio file and text")
parser.add_argument("audio_path", help="Path to the audio wave file")
parser.add_argument("text", help="Text or path to the text file")
args = parser.parse_args()

text = None

try:
    with open(args.text) as content_file:
        text = content_file.read()
except OSError as err:
    print("Can't find text file. Interpret as plain text")
    text = args.text

# process text
pattern = r"(\S.+?([.!?]|$))(?=\s+|$)"  # divide in sentences
sentences = re.findall(pattern, text)
for i in range(len(sentences)):
    if isinstance(sentences[i], tuple):
        sentences[i] = sentences[i][0]
number_of_sentences = len(sentences)

# select intervals
intervals = vad.get_silence_intervals(args.audio_path)
number_of_intervals = number_of_sentences + 1
intervals = sorted(intervals, key=lambda interval: interval.length())
intervals = intervals[len(intervals) - number_of_intervals:len(intervals)]
intervals = sorted(intervals, key=lambda interval: interval.start)

#create SubRip
speech_intervals = [None] * (len(intervals) - 1)
for i in range(len(intervals) - 1):
    speech_intervals[i] = vad.TimeInterval.between(intervals[i], intervals[i + 1])
subtitles = SubRip(speech_intervals, sentences)
path_to_subs = PurePath(args.audio_path).with_suffix(".srt")
with open(str(path_to_subs), 'w') as f:
    f.write(str(subtitles))




