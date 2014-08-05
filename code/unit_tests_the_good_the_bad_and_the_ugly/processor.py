import collections

Track = collections.namedtuple('Track', 'name, popularity')

class TracksProcessor:
    def __init__(self, top_amount):
        self._top_amount = top_amount

    def process(self, tracks):
        sorted_ = sorted(tracks, key=lambda track: track.popularity, reverse=True)

        return sorted_[:self._top_amount]
