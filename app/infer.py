#!/usr/bin/env python3
import argparse
from faster_whisper import WhisperModel
# from util_rttm import parse_rttm_file, convert2clip_timestamps
import util_rttm
# from util_lat import convert_to_lat, LatSegment
import util_lat
import schema
from typing import List


def transcribe_with_rttm(rttm_path:str, model:WhisperModel, input_path:str) -> List[schema.LatSegment]:
  rttm_segments = util_rttm.parse_rttm_file(rttm_path)
  clip_timestamps = util_rttm.convert2clip_timestamps(rttm_segments)
  whisper_segments, info = model.transcribe(input_path, word_timestamps=True, language="lt", clip_timestamps=clip_timestamps)
  lat_segments = util_lat.convert_to_lat(rttm_segments, whisper_segments)
  return lat_segments
   

def transcribe(model:WhisperModel, input_path:str):
  segments, info = model.transcribe(input_path, word_timestamps=True, language="lt")
  for segment in segments:
    # print(segment)
    #print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    for word in segment.words:
        #print("\t[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
        word_txt=word.word.strip() #rstrip(".").lstrip(" ")
        print("1 %.2f %.2f %s" % (word.start, word.end, word_txt))

   


if __name__ == "__main__":
  argparser = argparse.ArgumentParser(description='Semantika Ausis is client')
  # Optional positional argument
  argparser.add_argument('--input', '-i', type=str, required=True,
                      help='An required path to audio signal')
  
  argparser.add_argument('--rttm', '-r', type=str, nargs='?',
                    help='An option path to rttm segments')
  
  argparser.add_argument('--model', '-m', type=str, nargs='?', default="large-v3",
                    help='An option model name')

  args = argparser.parse_args()
  
  input_path = args.input #"audio-files/test.wav"
  model_name = args.model #"large-v3"
  # model_name = "mondhs/whisper-small-lt-liepa2_40_20-v6-ct2-int8"
  # model_name = "isLucid/faster-whisper-large-v2-20241031"
  model = WhisperModel(model_name, device="cuda")


  rttm_path = args.rttm
  clip_timestamps=None
  if rttm_path:
    lat_segments = transcribe_with_rttm(rttm_path, model, input_path)
    print(util_lat.convert_lat2txt(lat_segments))
  else:
    lat_segments =transcribe(model, input_path)
    print(util_lat.convert_lat2txt(lat_segments))
