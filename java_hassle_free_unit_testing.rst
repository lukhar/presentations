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
    public class TrackInfoLinkManagementControllerTest {

        public static final long ALBUM_ID = 1234567893058L;

        private TrackInfoLinkManagementService service;
        private TrackInfoLinkManagementController controller;

        @Before
        public setUp() {
            service = mock(TrackInfoLinkManagementService.class);
            controller = new TrackInfoLinkManagementController(service);
        }

       /**********
        *  ADD   *
        **********/

        @Test
        public void canAddTrackInfo() throws RestApiClientErrorException {
            String trackId = "xxx-1234";
            boolean active = false;
            TrackInfo trackInfo = new TrackInfo(ALBUM_ID, trackId);
            trackInfo.setActive(active);
            CreateTrackInfoLinkCommand command = 
                new CreateTrackInfoLinkCommand(ALBUM_ID, trackId, active);
            final TrackInfoResponse response = mock(TrackInfoResponse.class);
            when(service.addTrackInfoLink(trackInfo)).thenReturn(response);
            assertThat(controller.addTrackInfoLink(command), is(response));
            verify(service).addTrackInfoLink(trackInfo);
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

    public class TrackInfoLinkManagementControllerTest {

        public static final long ALBUM_ID = 1234567893058L;

        private TrackInfoLinkManagementService service;
        private TrackInfoLinkManagementController controller;

        @Before
        public setUp() {
            service = mock(TrackInfoLinkManagementService.class);
            controller = new TrackInfoLinkManagementController(service);
        }

        @Test
        public void canAddTrackInfo() throws RestApiClientErrorException {
            String trackId = "xxx-1234";
            boolean active = false;
            TrackInfo trackInfo = new TrackInfo(ALBUM_ID, trackId);
            trackInfo.setActive(active);

            CreateTrackInfoLinkCommand command = 
                new CreateTrackInfoLinkCommand(ALBUM_ID, trackId, active);
            TrackInfoResponse response = mock(TrackInfoResponse.class);
            when(service.addTrackInfoLink(trackInfo)).thenReturn(response);
            
            controllerResponse = controller.addTrackInfoLink(command)

            assertThat(controllerResponse, is(response));
            verify(service).addTrackInfoLink(trackInfo);
        }
    }

----

Not much of the help huh? True but we start to notice more now...
=================================================================

For example this fragment is not neccessary (and you don't even have to look into implementation):
    .. code-block:: java

        TrackInfoResponse response = mock(TrackInfoResponse.class);
        when(service.addTrackInfoLink(trackInfo)).thenReturn(response);

        assertThat(controllerResponse, is(response));

Moreover we can notice the connection between `trackInfo` and `command`
