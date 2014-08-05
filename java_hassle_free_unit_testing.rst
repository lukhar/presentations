:css: java_hassle_free_unit_testing.css
:title: Java: Hassle Free Unit Testing
:skip-help: true

.. title:: Java: Hassle Free Unit Testing

----

Java: Hassle Free Unit Testing
==============================
----

What I'll be talking about (this time)...
=========================================

* how to tackle Java verbosity in every day unit testing

* few tips about what tools use and how to use them

* throw in some remarks about naming conventions, common testing patterns etc...

----

Let's start with simple things...
=================================

.. code:: java

    /**
     * @author lukasz
     */
    public class TrackLinkManagementControllerTest {

        public static final long ALBUM_ID = 1234567893058L;

        private TrackLinkManagementService service;
        private TrackLinkManagementController controller;

        @Before
        public setUp() {
            service = mock(TrackLinkManagementService.class);
            controller = new TrackLinkManagementController(service);
        }

       /**********
        *  ADD   *
        **********/

        @Test
        public void canAddTrackLink() throws RestApiClientErrorException {
            String trackId = "xxx-1234";
            boolean active = false;
            TrackLink trackLink = new TrackLink(ALBUM_ID, trackId);
            trackLink.setActive(active);
            CreateTrackLinkCommand command = 
                new CreateTrackLinkCommand(ALBUM_ID, trackId, active);
            final TrackLink response = mock(TrackLinkResponse.class);
            when(service.addTrackLink(trackLink)).thenReturn(response);
            assertThat(controller.addTrackLink(command), is(response));
            verify(service).addTrackLink(trackLink);
        }
    }

----

Few things I've noticed
=======================

* hard to figure out what is behaviour is actually tested (everything is clattered, variable names are verbose but not descriptive...)

* obsolete comments ("Add", "author") *there's git for that...*

* mock returning mock brrr...  

* unnecessary finals here and there

* too verbose naming (putting *management* everywhere doesn't make names more descriptive)

----

Let's try to remove some of this clutter
========================================
.. code:: java

    public class TrackLinkManagementControllerTest {

        public static final long ALBUM_ID = 1234567893058L;

        private TrackLinkManagementService service;
        private TrackLinkManagementController controller;

        @Before
        public setUp() {
            service = mock(TrackLinkManagementService.class);
            controller = new TrackLinkManagementController(service);
        }

        @Test
        public void canAddTrackLink() throws RestApiClientErrorException {
            String trackId = "xxx-1234";
            boolean active = false;
            TrackLink trackLink = new TrackLink(ALBUM_ID, trackId);
            trackLink.setActive(active);

            CreateTrackLinkCommand command = 
                new CreateTrackLinkCommand(ALBUM_ID, trackId, active);
            TrackLinkResponse response = mock(TrackLinkResponse.class);
            when(service.addTrackLink(trackLink)).thenReturn(response);
            
            controllerResponse = controller.addTrackLink(command)

            assertThat(controllerResponse, is(response));
            verify(service).addTrackLink(trackLink);
        }
    }

----

Not much of the help huh? True but we start to notice more now...
=================================================================

For example this fragment is unnecessary (and you don't even have to look into implementation to figure that out ;)):
    .. code-block:: java

        TrackLinkResponse response = mock(TrackLinkResponse.class);
        when(service.addTrackLink(trackLink)).thenReturn(response);

        assertThat(controllerResponse, is(response));

Moreover we can notice the connection between :code:`trackLink` and :code:`command` now. Namely first one is expected result of processing :code:`command` object by :code:`controller` and it supposed to be passed to :code:`service`.

We can also spot bits of code that could use some renaming: 

    * :code:`canAddTrackLink` doesn't really tell us much about test

    * :code:`service`, :code:`command`, :code:`controller` could be more descriptive 

    * finally by using :code:`MockitoJUnitRunner` and proper annotations we can simplify test initialisation

----

So let's try simplify those bits even more 
==========================================
*and we still haven't touch objects interfaces btw ;-)*

.. code:: java

    @RunWith(MockitoJUnitRunner.class)
    public class TrackLinkManagementControllerTest {

        public static final long ANY_VALID_ALBUM_ID = 1234567893058L;
        public static final String ANY_VALID_TRACK_ID = "xxx-1234";

        @Mock
        private TrackLinkManagementService trackLinkServiceMock;
        @InjectMocks
        private TrackLinkManagementController trackLinkController;

        @Test
        public void verifyInactiveLinkAddition() throws RestApiClientErrorException {
            // given
            boolean active = false;
            TrackLink inactiveLink = new TrackLink(ANY_VALID_ALBUM_ID, ANY_VALID_TRACK_ID);
            inactiveLink.setActive(active);

            CreateTrackLinkCommand createTrackLinkCommand = 
                new CreateTrackLinkCommand(ANY_VALID_ALBUM_ID, trackId, active);

            // when 
            trackLinkController.addTrackLink(createTrackLinkCommand)

            // then
            verify(trackLinkServiceMock).addTrackLink(inactiveLink);
        }
    }

----

Now what if we had bit more time and freedom to modify interfaces as we like?
=============================================================================

.. code:: java

    @RunWith(MockitoJUnitRunner.class)
    public class TrackLinkControllerTest {

        public static final long ANY_VALID_ALBUM_ID = 1234567893058L;
        public static final String ANY_VALID_TRACK_ID = "xxx-1234";

        @Mock
        private TrackLinkService trackLinkServiceMock;
        @InjectMocks
        private TrackLinkController trackLinkController;

        @Test
        public void verifyInactiveLinkAddition() throws RestApiClientErrorException {
            // given
            TrackLink inactiveLink = aTrackLink
                .withTrackId(ANY_VALID_TRACK_ID).withAlbumId(ANY_VALID_ALBUM_ID)
                .setActive(false).build()

            CreateTrackLinkCommand createTrackLinkCommand = 
                aCreateTrackLinkComand.from(inactiveLink);

            // when 
            trackLinkController.addTrackLink(createTrackLinkCommand)

            // then
            verify(trackLinkServiceMock).addTrackLink(inactiveLink);
        }
    }
