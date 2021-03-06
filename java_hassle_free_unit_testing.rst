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

* hard to figure out what behaviour is actually tested (everything is clattered, variable names are verbose but not descriptive...)

* obsolete comments ("Add", "author"?  *there's git for that...*)

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

----

What have we achived? 
=====================

* more readable/maintainable test (hopefully)

* less lines of code to care about (yay!)

* and all of that without modifying production code (well almost...)

----

Now lets talk about tools and patterns which will make your life with unit tests easier
=======================================================================================

* value objects - how to implement them, common pitfalls

* Mockito - few tips on mocking/spying/stubbing

* custom assertions and matchers (Hamcrest vs FEST-Assert)

* testing exceptions

----

But first... a riddle ;)
========================

Given below code how many times :code:`MyTestedClass` constructor will be invoked during execution of this test?

.. code:: java

    public class SomeRandomTest {

        private MyTestedClass objectUnderTest = new MyTestedClass();

        @Test
        public void firstTest(){
           // ... 
        }

        @Test
        public void secondTest(){
           // ... 
        }
   }
   
----

Value objects or (in)famous POJOs 
==================================

* best served **immutable** (unfortunately designing immutable entities in Java is an art itself...)

* **always** provide :code:`hashCode`, :code:`equals` and :code:`toString` methods (preferably by using Guava or ApacheCommons or :code:`Objects` class for JDK7 and above)

* remember to provide **convenient way** (aka builder) to construct your object when it has more than 2,3 properties. *And no default constructor plus bunch of setters is not considered convenient (at least by me)*

----

Why not default methods generated by your IDE?
===============================================

* implementation differs across the IDEs (lack of consistency)

* usually expose gory details (especially in :code:`hashCode` implementations) 

* have I mentioned IntelliJ has plugins for all variations ;)

* also if you stick to immutable objects you can use reflection builders (available in ApacheCommons)

* finally in all cases it's less code to generate ;)

----

Few words about builders
========================

* you can provide builders for your value object by introducing **Object Mother**, **Builder as inner class** and **Builder as normal class**

* choice between inner or normal class builder is purely preferential (either more classes to cope with or bigger class definitions) 

* **Object Mother** provides betters readability but is less flexible, also in contrary to other builder patters it should be implement only in test code

* using **Inner Builder** allows you to precisely enforce how your object is constructed (by making default constructor of built class private)

* and again your IDE supports both **Outer** and **Inner** builder patterns - use it to our advantage ;)

----

Example of static inner builder (from uncle Bloch)
==================================================

.. code:: java

    public class NutritionalFacts {
        private int sodium;
        private int fat;
        private int carbo;

        public class Builder {
            private int sodium;
            private int fat;
            private int carbo;

            public Builder(int s) {
                this.sodium = s;
            }

            public Builder fat(int f) {
                this.fat = f;
                return this;
            }

            public Builder carbo(int c) {
                this.carbo = c;
                return this;
            }

            public NutritionalFacts build() {
                return new NutritionalFacts(this);
            }
        }

        private NutritionalFacts(Builder b) {
            this.sodium = b.sodium;
            this.fat = b.fat;
            this.carbo = b.carbo;
        }
    }

----

Faking it with Mockito
======================

* use :code:`MockitoJUnitRunner`, :code:`InjectMocks` and :code:`Mock` annotations, most of the time you (really) don't need :code:`setUp`, :code:`tearDown` methods

* :code:`Mock` annotation alone doesn't give you all that much... (seen few usages in our code)

* two styles of stubbing:
    * traditional: :code:`when`, :code:`thenReturn`, :code:`thenThrow`
    * BDD: :code:`given`, :code:`willReturn`, :code:`willThrow` 

----

Is Mockito really a mocking framework?
======================================

From Mockito site:

*There is a bit of confusion around the vocabulary. Technically speaking Mockito is a Test Spy framework. Usually developers use Mockito instead of a mocking framework. Test Spy framework allows to verify behaviour (like mocks) and stub methods (like good old hand-crafted stubs).*

* stub example:
  
    .. code:: java
       
        BankService serviceStub = mock(BankService.class) 
        given(serviceStub.getBalanceForCustomer("Lukasz")).willReturn("-10$")

* mock example:
    
    .. code:: java
       
        BankService serviceMock = mock(BankService.class) 
        verify(serviceMock).getBalanceForCustomer("Lukasz")

As you can see difference lays only in usage patterns.

----

Ok but when to mock/stub?
=========================

General guidelines are:

* *Mock across architecturally significant boundaries, but not within those boundaries.* Uncle Bob

* Mock only the code you have full control off.

* **Never** mock value objects.

----

It usally comes down to this
============================

.. image:: images/hexagonal_architecture_sketch.jpg

----

My rule of thumb...
===================

When in order to setup your test scenario you need:

     .. code:: java

          RadioStation station = new RadioStation.Builder()
            .withId("s9")
            .withName("station")
            .withDescription("description")
            .withImage(image_)
            .withCreator(user_)
            .withSeeds(Collections.<String>emptyList())
            .withSearchable(false)
            .withUserCreated(false)
            .create();

and *only few* of those properties are relevant for the test and yet *all* of them are needed... You *probably* have some functionally to abstract (and stub).

----

It usally comes down to this
============================

.. image:: images/hexagonal_architecture_sketch.jpg

----

My rule of thumb...
===================

When in order to setup your test scenario you need:

     .. code:: java
      RadioStation station = new RadioStation.Builder()
        .withId("s9")
        .withName("station")
        .withDescription("description")
        .withImage(image_)
        .withCreator(user_)
        .withSeeds(Collections.<String>emptyList())
        .withSearchable(false)
        .withUserCreated(false)
        .create();

and only few of those properties are relevant for the test and yet *all* of them are needed... You *probably* have some functionally to abstract (and stub).

Hamcrest vs FEST-Assert - functionally they're both the same 
=============================================================

  * Hamcrest:

     .. code:: java

         Biscuit theBiscuit = new Biscuit("Ginger");
         Biscuit myBiscuit = new Biscuit("Ginger");

         assertThat(theBiscuit, equalTo(myBiscuit));

  * FEST-Assert:

     .. code:: java

         Biscuit theBiscuit = new Biscuit("Ginger");
         Biscuit myBiscuit = new Biscuit("Ginger");

         assertThat(theBiscuit).isEqualTo(myBiscuit);

----

But devil's in the details
==========================

Thanks to fluent interface style invocation **FEST-Assert** gives us instant feedback about matchers available for given entity. At the same time finding available matchers with **Hamcrest** can be very frustrating... 

----


Exception testing idioms - expected paramter in @Test anotation or @Rule annotation
===================================================================================

     .. code:: java

        @Test(expected = CountryNotFoundException.class)
        public void givenNonExistingCountryRaiseCountryNotFoundException() {
            GDPCollaborator.prepare();
            GDPService.getIncomeFor("Seven Kingdoms");
        }

+ short and straightforward

- but impossible to verify from where the Exception has been thrown

    .. code:: java

        @Rule
        public ExpectedException exception = ExpectedException.none();

        @Test
        public void givenNonExistingCountryRaiseCountryNotFoundException() {
            thrown.expect(CountryNotFoundException.class);
            thrown.expectMessage("Not a country");
            GDPCollaborator.prepare();
            GDPService.getIncomeFor("Seven Kingdoms");
        }

+ bit more verbose but handy in complicated setups 

----

Exception testing idioms - try catch pattern
============================================

    .. code:: java

        @Test 
        public void givenNonExistingCountryRaiseCountryNotFoundException() {
            GDPCollaborator.prepare();
            
            try {
                GDPService.getIncomeFor("Seven Kingdoms");
                fail("CountryNotFoundException expected.");
            } catch (CountryNotFoundException expected) {
                // additional assertions
            } catch (Exception e) {
                fail("Unexpected exception " + e + " expected: CountryNotFoundException");
            }
        }

+ in contrary to previous examples we can easily pinpoint exception we mean to test and verify that no other exceptions where thrown

- it looks ugly isn't it?

----

Exception testing idioms - use catch-exception library
======================================================
    
    .. code:: java

        @Test 
        public void givenNonExistingCountryRaiseCountryNotFoundException() {
            GDPCollaborator.prepare() 

            GDPService.getIncomeFor("Seven Kingdoms")

            then(caughtException())
                .isInstanceOf(CountryNotFoundException.class)
                .hasMessage("Runtime exception occurred")
                .hasMessageStartingWith("Runtime")
                .hasMessageEndingWith("occured")
                .hasMessageContaining("exception")
                .hasNoCause();
        }

+ clean, robust follows Arrange Act Assert like testing conventions

+ this is my current way to go when testing exceptions

----


Thank you
=========

