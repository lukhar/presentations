from processor import TracksProcessor, Track
from nose.tools import assert_equals

class TestTracksProcessor:

    def test_aa001(self):
        tracks = [Track('test1', 0.5), Track('test2', 0.3), Track('test3', 0.9)]
        output = TracksProcessor(2).process(tracks)
        assert_equals(len(output), 2)
        assert_equals(output[0][1], 0.9)
        assert_equals(output[1][1], 0.5)

    def test_should_retrieve_top_two_popular_tracks(self):
        # given
        tracks = [Track(name='Genesis', popularity=0.5),
                  Track(name='American Idiot', popularity=0.3),
                  Track(name='Radioactive', popularity=0.9)]

        expected = [Track(name='Radioactive', popularity=0.9),
                    Track(name='Genesis', popularity=0.5)]

        # when
        top_popular_tracks = TracksProcessor(top_amount=2).process(tracks)

        # then
        assert_equals(top_popular_tracks, expected)
