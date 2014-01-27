import util.cache
import db

class TrackService:

    def similar_tracks(self, track_id, max_amout=100):
        if cache.contains(track_id):
            return cache.fetch_tracks(track_id)
        else:
            tracks = db.find_similar_tracks(track_id)
            cache.add(track_id, tracks)

            return tracks[:max_amout]

class TrackService:

    def __init__(self, cache, db):
        self._cache = cache
        self._db = db

    def similar_tracks(self, track_id, max_amout=100):
        if self._cache.contains(track_id):
            return self._cache.fetch_tracks(track_id)
        else:
            tracks = self._db.find_similar_tracks(track_id)
            self._cache.add(track_id, tracks)

            return tracks[:max_amout]
