from dataclasses import dataclass

from typing import Optional, List, Iterable

# import app.schema as schema 
import schema 
from faster_whisper.transcribe import Segment
import types



def convert_to_lat(rttm_segments:List[schema.RTTMSegment], whisper_segments:Iterable[Segment]) -> List[schema.LatSegment]:
    # print("whisper_segments is gen", isinstance(whisper_segments, types.GeneratorType))
    # if len(rttm_segments) != len(list(whisper_segment)):
    #     #rttm_segments({len(rttm_segments)}) =! whisper_segment({len(list(whisper_segment))})
    #     raise Exception("Segments count are not same")
    # print("whisper_segments: ", whisper_segments)
    result = []
    i=0
    for w_seg in whisper_segments:
      r_seg = rttm_segments[i]
      # print("w_segment1: ", w_seg)
      # print("r_seg: ", r_seg)
      # print("i: ", i)
      speaker = r_seg.speaker #r_seg.speaker
      tokens = []
      for w_word in w_seg.words:
         tokens.append(schema.LatToken(start_sec=w_word.start, end_sec=w_word.end, word_text=w_word.word, probability=w_word.probability))
      result.append(schema.LatSegment(speaker=speaker, sequence_no=w_seg.id, confidence=0, tokens=tokens))
      i=i+1
        
    # for r_seg, w_seg in zip(rttm_segments, whisper_segments):
    #     print("r_seg", r_seg)
    #     print("w_seg", w_seg)
        
        # i=i+1
    return result


def convert_lat2txt(lat_segments:List[schema.LatSegment]) -> str:
  string_buff = ""
  for l_seg in lat_segments:
      string_buff = string_buff+ f"# {l_seg.sequence_no} {l_seg.speaker}\n"
      for l_token in l_seg.tokens:
          string_buff = string_buff+ f"1 {l_token.start_sec} {l_token.end_sec} {l_token.word_text}\n"
      string_buff = string_buff+"\n"
  return string_buff