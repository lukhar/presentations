from trackservice import TrackService
from mock import patch
from mock import Mock
from nose.tools import assert_equals
from nose.tools import assert_true

class TestTrackService:

    @patch('trackservice.db')
    @patch('trackservice.cache')
    def test_should_retrieve_similar_tracks_from_db(self, cache_mock, db_mock):
        # given
        track_ids = [111, 222, 333, 444]
        expected_tracks = [111, 222, 333]
        cache_mock.contains.return_value = False
        db_mock.find_similar_tracks.return_value = track_ids

        # when
        similar_tracks = TrackService().similar_tracks(track_id, max_amout=3)

        # then
        assert_equals(similar_tracks, expected_tracks)
        assert_true(cache_mock.add.called)

    def setup()
        self.cache_mock = Mock()
        self.db_mock = Mock()

    def test_should_retrieve_similar_tracks_from_db(self):
        # given
        track_ids = [111, 222, 333, 444]
        expected_tracks = [111, 222, 333]
        self.cache_mock.contains.return_value = False
        self.db_mock.find_similar_tracks.return_value = track_ids

        # when
        similar_tracks = TrackService(self.cache_mock, self.db_mock)
                            .similar_tracks(track_id, max_amout=3)

        # then
        assert_equals(similar_tracks, expected_tracks)
        assert_true(self.cache_mock.add.called)
