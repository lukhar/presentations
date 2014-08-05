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

    public class ProfileServiceTest {

        private ProfileRepository profileRepositoryMock;
        private UserRepository userRepertoryMock;
        private ProfileService profileService;

        @Before
        public void setUp() {
           profileRepositoryMock = new mock(ProfileRepository.class);
           userRepertoryMock = new mock(userRepertoryMock.class);
           profileService = new ProfileService(profileRepositoryMock, userRepertoryMock)
        }

        @Test
        public void shouldNotCreateProfileWhenOneExistsInRepository() {
            // given
            User existingUser = User()
            exitingUser.setUserId("axf2345adf")

            Profile profileEntity = newProfile()
                    .withUser(existingUser)
                    .build();
            given(profileRepositoryMock.findByUserUserId(EXISTING_USER_ID))
                    .willReturn(profileEntity);

            // when
            Profile profile = profileService.createProfileForUser(existingUser);

            // then
            assertThat(profile.getUser()).isEqualTo(existingUser);
        }
    }
