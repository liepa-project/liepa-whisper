import re
from typing import Optional, List
# from .schema import RTTMSegment
import schema


def convert2clip_timestamps(segments:List[schema.RTTMSegment]) -> List[float]:
    clips = []
    for seg in segments:
        clips.append(seg.start)
        clips.append(seg.start+seg.duration)
    return clips


def parse_rttm_line(rttm_line: str) -> schema.RTTMSegment|None:
    parts = rttm_line.split()
    if len(parts) < 9:
        return None
    confidence = None
    if len(parts) > 8 and re.match(r'^\d+(\.\d+)?$', parts[5]):
        confidence = float(parts[5])
    return schema.RTTMSegment(
        file=parts[1],
        channel=parts[2],
        start=float(parts[3]),
        duration=float(parts[4]),
        speaker=parts[7],
        confidence=confidence,
        speech_type=parts[8],
        details=' '.join(parts[9:]) if len(parts) > 9 else ''
    )

def parse_rttm_lines(rttm_lines: List[str]) -> List[schema.RTTMSegment]:
    segments = []
    for line in rttm_lines:
        segment = parse_rttm_line(line)
        if segment:
            segments.append(segment)
    return segments


def parse_rttm_file(file_path: str) -> List[schema.RTTMSegment]:
    segments = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                segment = parse_rttm_line(line)
                if segment:
                    segments.append(segment)
                
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    return segments