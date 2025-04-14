import unittest
# from src.util_rttm import parse_rttm_file, parse_rttm_lines,convert2clip_timestamps, RTTMSegment
import app.util_rttm as util_rttm
import app.schema as schema
import os

class TestRTTMParser(unittest.TestCase):

    def setUp(self):
        self.dummy_rttm_content = """
        SPEAKER file1 1 0.5 2.0 <NA> <NA> speaker1 speech
        SPEAKER file1 1 2.5 1.5 <NA> <NA> speaker2 speech
        SPEAKER file2 1 0.0 3.0 <NA> <NA> speaker1 non-speech noise
        SPEAKER file1 1 4.0 1.0 0.98 <NA> speaker1 speech hello world
        """
        with open("test.rttm", "w") as f:
            f.write(self.dummy_rttm_content)

    def tearDown(self):
        if os.path.exists("test.rttm"):
            os.remove("test.rttm")

    def test_convert2clip_timestamps(self):
        segments=[schema.RTTMSegment(file='', channel='', start=0.0, duration=5.279, speaker='SPEAKER_02', confidence=None, speech_type='', details=''),
schema.RTTMSegment(file='', channel='', start=5.279, duration=5.088, speaker='SPEAKER_00', confidence=None, speech_type='', details=''),
schema.RTTMSegment(file='', channel='', start=10.367, duration=4.423, speaker='SPEAKER_02', confidence=None, speech_type='', details=''),
schema.RTTMSegment(file='', channel='', start=21.755, duration=7.507, speaker='SPEAKER_01', confidence=None, speech_type='', details='')]
        result=util_rttm.convert2clip_timestamps(segments)
        self.assertEqual(len(result), 8)



    def test_parse_valid_rttm_lines(self):
        rttm_lines = """
        SPEAKER file1 1 0.5 2.0 <NA> <NA> speaker1 speech
        SPEAKER file1 1 2.5 1.5 <NA> <NA> speaker2 speech
        SPEAKER file2 1 0.0 3.0 <NA> <NA> speaker1 non-speech noise
        SPEAKER file1 1 4.0 1.0 0.98 <NA> speaker1 speech hello world
        """.split("\n")
        segments = parse_rttm_lines(rttm_lines)
        self.assertEqual(len(segments), 4)
        self.assertEqual(segments[0], schema.RTTMSegment(file='file1', channel='1', start=0.5, duration=2.0, speaker='speaker1', confidence=None, speech_type='speech', details=''))
        self.assertEqual(segments[1], schema.RTTMSegment(file='file1', channel='1', start=2.5, duration=1.5, speaker='speaker2', confidence=None, speech_type='speech', details=''))
        self.assertEqual(segments[2], schema.RTTMSegment(file='file2', channel='1', start=0.0, duration=3.0, speaker='speaker1', confidence=None, speech_type='non-speech', details='noise'))
        self.assertEqual(segments[3], schema.RTTMSegment(file='file1', channel='1', start=4.0, duration=1.0, speaker='speaker1', confidence=0.98, speech_type='speech', details='hello world'))

    def test_parse_valid_rttm_lines(self):
        rttm_lines = """
        SPEAKER file 1 0.000 5.279 <NA> <NA> SPEAKER_02 <NA> <NA>
        SPEAKER file 1 5.279 5.088 <NA> <NA> SPEAKER_00 <NA> <NA>
        SPEAKER file 1 10.367 4.423 <NA> <NA> SPEAKER_02 <NA> <NA>
        SPEAKER file 1 21.755 7.507 <NA> <NA> SPEAKER_01 <NA> <NA>
        """.split("\n")
        segments = util_rttm.parse_rttm_lines(rttm_lines)
        self.assertEqual(len(segments), 4)
        self.assertEqual(segments[0], RTTMSegment(file='file', channel='1', start=0.0, duration=5.279, speaker='SPEAKER_02', confidence=None, speech_type='<NA>', details='<NA>'))
        self.assertEqual(segments[1], RTTMSegment(file='file', channel='1', start=5.279, duration=5.088, speaker='SPEAKER_00', confidence=None, speech_type='<NA>', details='<NA>'))
        self.assertEqual(segments[2], RTTMSegment(file='file', channel='1', start=10.367, duration=4.423, speaker='SPEAKER_02', confidence=None, speech_type='<NA>', details='<NA>'))
        self.assertEqual(segments[3], RTTMSegment(file='file', channel='1', start=21.755, duration=7.507, speaker='SPEAKER_01', confidence=None, speech_type='<NA>', details='<NA>'))


    def test_parse_valid_rttm(self):
        segments = util_rttm.parse_rttm_file("test.rttm")
        self.assertEqual(len(segments), 4)
        self.assertEqual(segments[0], RTTMSegment(file='file1', channel='1', start=0.5, duration=2.0, speaker='speaker1', confidence=None, speech_type='speech', details=''))
        self.assertEqual(segments[1], RTTMSegment(file='file1', channel='1', start=2.5, duration=1.5, speaker='speaker2', confidence=None, speech_type='speech', details=''))
        self.assertEqual(segments[2], RTTMSegment(file='file2', channel='1', start=0.0, duration=3.0, speaker='speaker1', confidence=None, speech_type='non-speech', details='noise'))
        self.assertEqual(segments[3], RTTMSegment(file='file1', channel='1', start=4.0, duration=1.0, speaker='speaker1', confidence=0.98, speech_type='speech', details='hello world'))

    def test_parse_empty_rttm(self):
        with open("empty.rttm", "w") as f:
            f.write("")
        segments = util_rttm.parse_rttm_file("empty.rttm")
        self.assertEqual(len(segments), 0)
        os.remove("empty.rttm")

    def test_parse_rttm_with_extra_fields(self):
        extra_content = "SPEAKER file3 1 1.0 2.0 <NA> <NA> speaker3 speech extra field\n"
        with open("extra.rttm", "w") as f:
            f.write(extra_content)
        segments = util_rttm.parse_rttm_file("extra.rttm")
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0], schema.RTTMSegment(file='file3', channel='1', start=1.0, duration=2.0, speaker='speaker3', confidence=None, speech_type='speech', details='extra field'))
        os.remove("extra.rttm")

    def test_parse_rttm_with_confidence(self):
        confidence_content = "SPEAKER file4 1 0.0 1.0 0.75 <NA> speaker4 speech\n"
        with open("confidence.rttm", "w") as f:
            f.write(confidence_content)
        segments = util_rttm.parse_rttm_file("confidence.rttm")
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0], schema.RTTMSegment(file='file4', channel='1', start=0.0, duration=1.0, speaker='speaker4', confidence=0.75, speech_type='speech', details=''))
        os.remove("confidence.rttm")

    def test_parse_nonexistent_file(self):
        segments = util_rttm.parse_rttm_file("nonexistent.rttm")
        self.assertEqual(len(segments), 0)

    def test_parse_malformed_line(self):
        malformed_content = "SPEAKER file5 1 0.0 1.0 speaker5 speech\n"
        with open("malformed.rttm", "w") as f:
            f.write(malformed_content)
        segments = util_rttm.parse_rttm_file("malformed.rttm")
        self.assertEqual(len(segments), 0)
        os.remove("malformed.rttm")

if __name__ == '__main__':
    unittest.main()
