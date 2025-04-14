from typing import Optional, List
from dataclasses import dataclass

@dataclass
class LatToken:
    start_sec: float
    end_sec: float
    word_text: str
    probability: Optional[float]


@dataclass
class LatSegment:
    speaker: str
    sequence_no: int
    confidence: Optional[float]
    tokens: Optional[List[LatToken]]



@dataclass
class RTTMSegment:
    file: str
    channel: str
    start: float
    duration: float
    speaker: str
    confidence: Optional[float]
    speech_type: str
    details: str

