import unittest
# from src.util_rttm import RTTMSegment
# from src.util_lat import LatSegment, convert_to_lat
from faster_whisper.transcribe import Segment, Word

import app.util_lat as util_lat
import app.schema as schema
import os

class TestLatParser(unittest.TestCase):

    def test_convert_to_lat(self):
        rttm_segments=[schema.RTTMSegment(file='', channel='', start=0.0, duration=5.279, speaker='SPEAKER_02', confidence=None, speech_type='', details=''),
            schema.RTTMSegment(file='', channel='', start=5.279, duration=5.088, speaker='SPEAKER_00', confidence=None, speech_type='', details=''),
            schema.RTTMSegment(file='', channel='', start=10.367, duration=4.423, speaker='SPEAKER_02', confidence=None, speech_type='', details=''),
            schema.RTTMSegment(file='', channel='', start=21.755, duration=7.507, speaker='SPEAKER_01', confidence=None, speech_type='', details='')]
        
        whisper_words = [Word(start=0.0, end=5.279, word="AAA", probability=1)]

        whisper_segment=[Segment(id=1,seek=1, start=0.0, end=5.279, text="long",tokens=[],avg_logprob=1, compression_ratio=1, no_speech_prob=1, words=[],temperature=1),
                         Segment(id=1,seek=1, start=5.279, end=10.367, text="long",tokens=[],avg_logprob=1, compression_ratio=1, no_speech_prob=1, words=[],temperature=1),
                         Segment(id=1,seek=1, start=10.367, end=21.755, text="long",tokens=[],avg_logprob=1, compression_ratio=1, no_speech_prob=1, words=[],temperature=1),
                         Segment(id=1,seek=1, start=21.755, end=27.179, text="long",tokens=[],avg_logprob=1, compression_ratio=1, no_speech_prob=1, words=whisper_words,temperature=1)
                         ]
        result=util_lat.convert_to_lat(rttm_segments, whisper_segment)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].speaker, rttm_segments[0].speaker)
        self.assertEqual(result[1].speaker, rttm_segments[1].speaker)
        self.assertEqual(result[2].speaker, rttm_segments[2].speaker)
        self.assertEqual(result[3].speaker, rttm_segments[3].speaker)
        self.assertEqual(result[3].tokens[0].start_sec, 0)
        self.assertEqual(result[3].tokens[0].end_sec, 5.279)
        self.assertEqual(result[3].tokens[0].word_text, "AAA")
        self.assertEqual(result[3].tokens[0].probability, 1)




if __name__ == '__main__':
    unittest.main()




    # def test__convert_to_lat__not_equal(self):
    #     rttm_segments=[RTTMSegment(file='', channel='', start=0.0, duration=5.279, speaker='SPEAKER_02', confidence=None, speech_type='', details=''),
    #         RTTMSegment(file='', channel='', start=5.279, duration=5.088, speaker='SPEAKER_00', confidence=None, speech_type='', details=''),
    #         RTTMSegment(file='', channel='', start=10.367, duration=4.423, speaker='SPEAKER_02', confidence=None, speech_type='', details=''),
    #         RTTMSegment(file='', channel='', start=21.755, duration=7.507, speaker='SPEAKER_01', confidence=None, speech_type='', details='')]
        
    #     whisper_segment=[]
    #     with self.assertRaises(Exception) as context:
    #         convert_to_lat(rttm_segments, whisper_segment)
        # self.assertTrue('Segments count are not same' in context.exception)