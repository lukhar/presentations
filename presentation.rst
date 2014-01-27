:css: presentation.css
:title: Unit Tests: The Good, The Bad and The Ugly
:skip-help: true

.. title:: Unit Tests: The Good, The Bad and The Ugly

----

Unit Tests: The Good, The Bad and The Ugly
==========================================
----

What I'll be talking about...
=============================

* my observations on how to make your tests easier to read/maintain

* few words about most common bad habits when unit testing

* summarize how the proper unit test should look like

----

Can you tell what exactly I’m testing here?
===========================================

.. code:: python

    from processor import TracksProcessor, Track
    from nose.tools import assert_equals

    class TestTracksProcessor:

        def test_aa001(self):
            tracks = [Track('test1', 0.5), Track('test2', 0.3),
                      Track('test3', 0.9)]
            output = TracksProcessor(2).process(tracks)
            assert_equals(len(output), 2)
            assert_equals(output[0][1], 0.9)
            assert_equals(output[1][1], 0.5)

----

It's nothing fancy really...
==============================

.. code:: python

    import collections

    Track = collections.namedtuple('Track', 'name, popularity')

    class TracksProcessor:
        def __init__(self, top_amount):
            self._top_amount = top_amount

        def process(self, tracks):
            sorted_ = sorted(tracks, key=lambda track: track.popularity,
                             reverse=True)

            return sorted_[:self._top_amount]

----

So... what's all that fuzz about?
=================================

test_aa01 isn't that bad actually:

    * it tests only one thing at a time

    * it tests functionality and don't care about implementation

    * it's fast; doesn't rely on external dependencies

having said that we still needed to spend considerable time understand what’s going on right?

----

How about making it more readable then?
=======================================

.. code:: python

    from processor import TracksProcessor, Track
    from nose.tools import assert_equals

    class TestTracksProcessor:
        def test_should_retrieve_top_two_popular_tracks(self):
            # given
            tracks = [Track(name='Genesis', popularity=0.5),
                      Track(name='American Idiot', popularity=0.3),
                      Track(name='Radioactive', popularity=0.9)]

            expected = [Track(name='Radioactive', popularity=0.9),
                        Track(name='Genesis', popularity=0.5)]

            # when
            top_popular_tracks = TracksProcessor(top_amount=2)
                                    .process(tracks)

            # then
            assert_equals(top_popular_tracks, expected)

----

What we've gained actually?
===========================

* we’re able to tell what part of functionality is tested just by looking at test method name
* we (usually) don’t have to jump around test/implementation to understand what tested code is doing
* we have exact use case of the code we might want reuse in the future
* test code is now documenting production code for us

----

Yeah I know it looks nice on paper but quite often we have to deal with this...
===============================================================================

.. code:: python

    import util.cache
    import db

    class TrackService:

        def similar_tracks(self, track_id):
            if cache.contains(track_id):
                return cache.fetch_tracks(track_id)
            else:
                tracks = db.find_similar_tracks(track_id)
                cache.add(track_id, tracks)

                return tracks

but in much more elaborated form of course ;)

----

So... how can we approach testing?
==================================

1. Setup test environment without touching internal representation of tested class/module.

2. Use python super powers and patch internals of test class/module.

3. Inject modules used directly inside the class as dependencies.

----

Setting up test environment
===========================

pros:
    + tests are independent of tested class/module implementation
cons:
    - tests became dependent on environment (ex. used database)
    - tests tend to be slow and complicated
    - to sum up we’re creating not unit but integration tests...

----

:id: patching-internal-representation

Patching internal representation
================================

.. code:: python

    from trackservice import TrackService
    from mock import patch
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
            similar_tracks = TrackService().similar_tracks(track_id, max_amount=3)

            # then
            assert_equals(similar_tracks, expected_tracks)
            assert_true(cache.add.called)

----

Looks nice right?
=================

It's definitely a proper unit test:

    * we test only part of the functionality at a time

    * we've clearly separated tested part of code from external dependencies

    * it's much faster then using environment with proper cache and database abstractions

Moreover thanks to @patch decorator it's really easy to implement.

----

However...
==========

What happens if we just change import style in trackservice from:

.. code:: python

    import util.cache

to:

.. code:: python

   from util import cache

?

----

Yep our beautiful test will fail miserably...
=============================================

Unfortunately monkey patching has some serious drawbacks:

* we're exposing feature implementation in tests making it harder to maintain/develop

* tests become fragile

* monkey patching promotes bad design practices; creating less modular more coupled code

----

Can we avoid patching? How about refactoring our class a little bit?
====================================================================

.. code:: python

    class TrackService:

        def __init__(self, cache, db):
            self._cache = cache
            self._db = db

        def similar_tracks(self, track_id, max_amount=100):
            if self._cache.contains(track_id):
                return self._cache.fetch_tracks(track_id)
            else:
                tracks = self._db.find_similar_tracks(track_id)
                self._cache.add(track_id, tracks)

                return tracks[:max_amout]

----

And fixing tests
================

.. code:: python

    class TestTrackService:

        def setup(self):
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
                                .similar_tracks(track_id, max_amount=3)

            # then
            assert_equals(similar_tracks, expected_tracks)
            assert_true(self.cache_mock.add.called)

----

What we've gained?
==================

* cleaner design; modules are loosely coupled now

* we're not exposing functionality implementation details to the tests

* more stable test suit

----

Few words about bad habits
==========================

Be descriptive, names like:

.. code:: python

    test_add()
    test_return_correct_value()
    test_abc23()

doesn't really tell you much.


Invocations like:

.. code:: python

    PlaylistGenerator(100, 54, False)
    calculate_salary(4000, 0.3, 2.3)

unnecessarily force reader to look into implementation.

Testing privates:

.. code:: python

    # ...
    self.processor._sort(tracks)
    # ...

binds your tests with implementation.

----

Fragile assertions
==================

You don't really want to do that:

.. code:: python

    # ...
    soap_message = response.to_soap()

    assert_equals(soap_message,
            '<soap:Envelope'
            ' xmlns:soap="http://www.w3.org/2001/12/soap-envelope"'
            ' soap:encodingStyle="http://www.w3.org/2001/12/soap-encoding"> '
            ' <soap:Body xmlns:m="http://www.example.org/stock">'
            '  <m:GetStockPriceResponse>'
            '    <m:Price>34.5</m:Price>'
            '  </m:GetStockPriceResponse>'
            ' </soap:Body>'
            '</soap:Envelope>')

----

Walking happy path
==================

.. code:: python

    def test_division():
        assert_equals(2, divide(4,2))
        assert_equals(-3, divide(-9,3))

Sooner or later someone tries to divide by zero so... it would be good to have this case covered.


----

To wrap up... a good unit test
==============================

* tests functionality not implementation

* tests single behavior

* isolates tested behavior

* clearly identifies any reason of failure

* documents expected behavior

* runs quickly

----

Thank you
=========
