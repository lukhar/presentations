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

* obsolete comments: "Add"?, if i'd like to know who is the author I just invoke git-blame...
* mock returning mock brrr...  
