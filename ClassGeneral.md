# General Principles #

**Original Principles**
  * The GUI should be manageable by novice users.  This entails as few buttons as possible with descriptive labels.  Additionally, tooltips should be included for teachers/parents for every major function to provide a good description of what everything does.

  * No more than six buttons should be used to navigate through the audio interface.  Buttons should perform in a consistent, predictable fashion at all times.

  * It is expected that the teacher will be launching the program and navigate to story creation.  It is also expected that the teacher will either not be visually impaired or be capable of navigating through a GUI with JAWS.

  * It is expected that the students creating stories may be visually impaired, so the interface is designed to accommodate their needs using audio prompts.

  * All common interactions should be designed with a novice computer user in mind.  File interactions, such as when a user prioritizes sounds in the library, should be simple and not assume any knowledge or understanding of directory structure or other advanced topics.  More advanced interactions can assume a higher level of understanding with support from detailed manual instructions.

  * The entire program should be kept simple - avoid "modes" and heavy modularization of the design.

  * Two uses should be kept in mind throughout design - "free" and "guided" use.  While the primary purpose is educational with the classroom and teacher templates in mind, users should be able to create stories from scratch without limits on the sound effects they can use.

**Global Objects**

Due to the complex interactions between objects in our design (i.e., some interfaces have both a GUI and an AUI), we store most of our objects in a dictionary called env that is passed to most of the objects.  Thus, almost any object can access any other object.  Env also keeps track of the functions for key bindings so that control can be more easily passed between objects.

**Key Bindings**

We chose to use a minimal number of prominent keys near the edges of the keyboard.  We also attempted to make the function of the keys consistent throughout the application as well as with Hark the Sound.  Specific key bindings can be found in the user manual.  All key bindings are done using dictionaries keyed by the key code that return a function to be executed for the key press.

**Sounds**

All sounds that are playing should be interruptible by a valid key press.